# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django import forms
from django.contrib.auth.models import Group

try:
    import simplejson as json
except ImportError:
    from django.utils import simplejson as json

from mtcompono.dynamo_form import DynamoForm, TemplateField
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
                                      
class EditType(DynamoForm):
    name = forms.CharField(widget=forms.HiddenInput)
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body", widget=forms.Textarea(
                                                attrs={'cols':80, 'rows':5,
                                                        'id': "body"}))
    templates = TemplateField(label="Template", required=False,
                        widget=TemplateWidget(attrs={'cols':100, 
                                                'rows':20}))
                                                
    class Meta:
        document = Page
        exclude = ['page_type', 'groups', 'ctype', 'need_edit','draft',
                    'created', 'updated']
                       
    