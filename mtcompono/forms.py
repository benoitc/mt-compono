# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django.contrib.auth.models import Group
from django import forms
from django.forms.util import ValidationError, ErrorList
from django.utils.datastructures import SortedDict

try:
    import simplejson as json
except ImportError:
    from django.utils import simplejson as json

from mtcompono.models import Type, Page
from mtcompono.widgets import TemplateWidget


FIELD_TYPES = {
    "Text": (forms.CharField,),
    "LongText": (forms.CharField, forms.Textarea,),
    "Date": (forms.CharField,)
}

                
class CreatePageType(forms.Form):
    path = forms.CharField(widget=forms.HiddenInput)
    page_type = forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        super(CreatePageType, self).__init__(*args, **kwargs)
        choices = [
                        ('type', 'Create from a new page type'),
                        ('context', 'Create a context page'),
                        ('--', '--'),
                        ('--', 'Create from exisiting type:'),
                        ('--', '--'),
                    ]
        choices += [(t._id, t.name) for t in Type.all()]
        
        self.fields['page_type'].choices =choices
        
class EditContext(forms.Form):
    title = forms.CharField(max_length=255)
    body = forms.CharField(label="Body", widget=forms.Textarea(
                                                attrs={'cols':80, 'rows':5,
                                                        'id': "body"}))
    editors = forms.MultipleChoiceField(
        label="Associate groups of editors to this page:",
        widget=forms.SelectMultiple(attrs={'size': 5, 'class': "multiselect"})
    )
    
    def __init__(self, *args, **kwargs):
        super(EditContext, self).__init__(*args, **kwargs)
        self.fields['editors'].choices = [
            (g.name, g.name) for g in Group.objects.all()]
            
            

EXTRA_PROPERTIES_MAPPING = {
    'text': (forms.CharField, None, None),
    'textarea': (forms.CharField, forms.Textarea, {'class': 'txt'}),
    'datetime': (forms.CharField, forms.TextInput, {'class': 'date'})
}


class EditContent(forms.Form):
    title = forms.CharField(max_length=255)
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, type_instance=None, 
                 document_instance=None):
         
        initial = initial or {}
        object_data = {}        
        self.extra_fields = SortedDict()
        self.type_instance = type_instance
        self.document_instance = document_instance
        if type_instance is not None and hasattr(type_instance, 'props'):
            for prop in type_instance.props:
                f, w, a = EXTRA_PROPERTIES_MAPPING[prop['name']]
                if not w:
                    field = f(label=prop['label'])
                else:
                    field = f(label=prop['label'], widget=w(attrs=a))
                self.extra_fields[prop['id']] = field
                if not document_instance:
                    continue
                else:
                    try:
                        object_data[prop['id']]= getattr(document_instance, 
                                                prop['id'])
                    except AttributeError:
                        continue
                        
        object_data.update(initial)
        
        super(EditContent, self).__init__(data=data, files=files, 
                auto_id=auto_id, prefix=prefix, initial=object_data,
                error_class=error_class, label_suffix=label_suffix, 
                empty_permitted=empty_permitted)
    
        if self.extra_fields:
            for name, field in self.extra_fields.items():
                self.fields[name] = field
        
    def save(self):
        cleaned_data = self.cleaned_data.copy()
        print cleaned_data
        for propname, value in cleaned_data.items():
            setattr(self.document_instance, propname, value)
            
        self.document_instance.save()
        return self.document_instance
                       
    