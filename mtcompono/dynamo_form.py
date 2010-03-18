# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

import base64

from django.forms.util import ValidationError, ErrorList
from django.forms.forms import BaseForm, get_declared_fields, BoundField
from django import forms
from django.utils.datastructures import SortedDict

try:
    import simplejson as json
except ImportError:
    from django.utils import simplejson as json

from mtcompono.widgets import TemplateWidget

class TemplateField(forms.Field):
    widget = TemplateWidget
    

_patched_ext = False
def patch_ext():
    global _patched_ext
    if _patched_ext:
        return
    from couchdbkit.ext.django.forms import FIELDS_PROPERTES_MAPPING
    FIELDS_PROPERTES_MAPPING.update({"DictProperty": TemplateField})
    _patched_ext = True
    
patch_ext()
    
from couchdbkit.ext.django.forms import DocumentForm

from mtcompono.models import Page

EXTRA_PROPERTIES_MAPPING = {
    'Text': (forms.CharField, None, None),
    'LongText': (forms.CharField, forms.Textarea, {'class': 'txt'}),
    'Date': (forms.CharField, forms.TextInput, {'class': 'date'})
}

DATA_EXTRA_MAPPING = {
    't': (forms.CharField, None, None),
    'ta': (forms.CharField, forms.Textarea, {'class': 'txt'}),
    'd': (forms.CharField, forms.TextInput, {'class': 'date'})
}

DATA_PROPERTIES_MAPPING = {
    't': 'Text',
    'ta': 'LongText',
    'd': 'Date'
}


class DynamoForm(DocumentForm):
    """ Base Document Form object """
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
            initial=None, error_class=ErrorList, label_suffix=":",
            empty_permitted=False, instance=None):
            
        self.extra_fields = SortedDict()
        initial = initial or {}
        object_data = {}
        extra_fields_keys = []
        
        if instance is not None and hasattr(instance, 'extra_properties'):
            for k, v in instance.extra_properties:
                f, w, a = EXTRA_PROPERTIES_MAPPING[v['name']]
                if not w:
                    field = f(label=v['label'])
                else:
                    field = f(label=v['label'], widget=w(attrs=a))
                self.extra_fields[k] = (field, forms.CharField())
                
                object_data['custom_%s' % k] =  v['value']
                object_data['lcustom_%s' % k] = v['label']
                extra_fields_keys.append(k)


        object_data.update(initial)
        
        super(DynamoForm, self).__init__(data=data, files=files, 
                    auto_id=auto_id, prefix=prefix, initial=object_data, 
                    error_class=error_class, label_suffix=label_suffix,
                    empty_permitted=empty_permitted, instance=instance)   
                    
        
        if self.extra_fields:
            for name, fields in self.extra_fields.items():              
                fname = 'custom_%s' % name
                if data is not None and fname not in data:
                    # fields have been deleted when editing
                    del self.extra_fields[name]
                    continue
                f, l = fields   
                self.fields[fname] = f
                self.fields['lcustom_%s' % name] = l
                       
        if data:
            for k, v in data.items():
                if k.startswith('custom_'):
                    try:
                        _, key = k.split('_', 1)
                        if key in self.extra_fields:
                            continue       
                        t, i = key.split('_')
                        f, w, a = DATA_EXTRA_MAPPING[t]  
                        if not w:
                            field = f()
                        else:
                            field = f(widget=w(attrs=a))
                        self.fields['custom_%s' % key] = field
                        self.fields['lcustom_%s' % key] = forms.CharField()
                        self.extra_fields[key] = (field, forms.CharField())
                    except (ValueError, KeyError):
                        continue                                          
    
    def extra_properties(self):
        for name, fields in self.extra_fields.items():
            f, l = fields
            yield (BoundField(self, f, "custom_%s" % name), 
                BoundField(self, l, "lcustom_%s" % name))
                    
    def save(self, commit=True):
        """
        Saves this ``form``'s cleaned_data into document instance
        ``self.instance``.

        If commit=True, then the changes to ``instance`` will be saved to the
        database. Returns ``instance``.
        """
        
        print "cleaned_data %s " % str(self.cleaned_data.items())
        opts = self._meta
        cleaned_data = self.cleaned_data.copy()
        for prop_name in self.instance._doc.keys():
            if opts.properties and prop_name not in opts.properties:
                continue
            if opts.exclude and prop_name in opts.exclude:
                continue
            if prop_name in cleaned_data:
                value = cleaned_data.pop(prop_name)
                if value is not None:
                    setattr(self.instance, prop_name, value)

        # fetch extra properties 
        extra_properties_dict = {}
        cleaned_keys = cleaned_data.keys()
        cleaned_keys.sort()
        for attr_name in cleaned_data.keys():
            if attr_name.startswith('custom_') or \
                    attr_name.startswith('lcustom_'):
                self.initial[attr_name] = cleaned_data[attr_name]
                
                key = attr_name.split('_', 1)[1]
                if key not in extra_properties_dict.keys():
                    v = {}
                else:
                    v = extra_properties_dict[key]
                    
                if attr_name[0] == "l":
                    v.update({"label": cleaned_data[attr_name]})
                else:
                    t, i = key.split('_')
                    v.update({
                        "value": cleaned_data[attr_name],
                        "name": DATA_PROPERTIES_MAPPING[t]
                    })                  
                extra_properties_dict[key] = v
                
        extra_properties = []
        for k in self.extra_fields.keys():
            if k in extra_properties_dict:
                extra_properties.append((k, extra_properties_dict[k]))

        if extra_properties:
            setattr(self.instance, "extra_properties", extra_properties)

        if commit:
            self.instance.save()
        
        return self.instance