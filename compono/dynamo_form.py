# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django.forms.util import ValidationError, ErrorList
from django.forms.forms import BaseForm, get_declared_fields
from django.forms import fields as f

from couchdbkit.ext.django.forms import DocumentForm


from compono.models import Page

EXTRA_PROPERTIES_MAPPING = {
    'Text': (f.CharField, None, None),
    'LongText': (f.CharField, f.ChoiceField),
    'Date': (f.CharField, None, {'class': 'date'})
}


class DynamoForm(DocumentForm):
    """ Base Document Form object """
    
    def __init__(self, *args, **kwargs):

        super(DynamoForm, self).__init__(*args, **kwargs)
        self.extra_fields = []                                
        if hasattr(self.instance, 'extra_properties'):
            for k, v in self.instance.extra_properties:
                f, w, a = EXTRA_PROPERTIES_MAPPING[v['name']]  
                if not w:
                    field = f(label=v['label'])
                else:
                    field = f(label=v['label'], widget=w(attrs=a))
                self.fields['custom_%s' % k] = field
                self.extra_fields.append(field)
                                              
                                            
    def save(self, commit=True):
        """
        Saves this ``form``'s cleaned_data into document instance
        ``self.instance``.

        If commit=True, then the changes to ``instance`` will be saved to the
        database. Returns ``instance``.
        """
        
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
        for attr_name in cleaned_data.keys():
            print attr_name
            if attr_name.startswith('custom_'):
                key = attr_name.split('custom_')[1]
                try:
                    extra_properties_dict[key]['value'] = cleaned_data[
                                                                attr_name]
                except KeyError:
                    extra_properties_dict[key] = {
                        'value': cleaned_data[attr_name]}
            elif attr_name.startswith('lcustom_'):
                try:
                    extra_properties_dict[key]['label'] = cleaned_data[
                                                                attr_name]
                except KeyError:
                    extra_properties_dict[key] = {
                        'label': cleaned_data[attr_name]}
        
        
        extra_keys = extra_properties_dict.keys()
        extra_keys.sort()       
        extra_properties = [(k, extra_properties_dict[k]) for k in extra_keys]
        if extra_properties:
            setattr(self.instance, "extra_properties", extra_properties)

        if commit:
            self.instance.save()
        
        return self.instance