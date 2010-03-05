# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from couchdbkit.ext.django.forms import DocumentForm
from django import forms
from django.contrib.auth.models import Group

from compono.dynamo_form import DynamoForm
from compono.models import Page


FIELD_TYPES = {
    "Text": (forms.CharField,),
    "LongText": (forms.CharField, forms.Textarea,),
    "Date": (forms.CharField,)
}

class CreatePage(forms.Form):
    path = forms.CharField(widget=forms.HiddenInput)
    page_type = forms.ChoiceField(choices=(
                    ('page', 'Create a page'),
                    ('context', 'Create a context page')
                ))
    editors = forms.MultipleChoiceField(widget=forms.SelectMultiple(
                                                        attrs={'size': 6}))
    
    def __init__(self, *args, **kwargs):
        super(CreatePage, self).__init__(*args, **kwargs)
        self.fields['editors'].choices =  [(g.name, g.name) \
                                                for g in Group.objects.all()]
                                      
class EditPage(DynamoForm):
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body", widget=forms.Textarea(
                                                attrs={'cols':80, 'rows':5}))
    template = forms.CharField(label="Template", required=False,
                        widget=forms.Textarea(attrs={'cols':100, 'rows':20}))
                                                
    class Meta:
        document = Page
        exclude = ['page_type', 'groups', 'ctype', 'need_edit','draft',
                    'created', 'updated']
                       
    