# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django import forms
from django.contrib.auth.models import Group

def list_groups():
    return [(g.name, g.name) for g in Group.objects.all()]

class CreatePage(forms.Form):
    path = forms.CharField(widget=forms.HiddenInput)
    page_type = forms.ChoiceField(choices=(
                    ('page', 'Create a page'),
                    ('context', 'Create a context page')
                ))
    editors = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': 6}))
    
    def __init__(self, *args, **kwargs):
        super(CreatePage, self).__init__(*args, **kwargs)
        self.fields['editors'].choices =  [(g.name, g.name) \
                                                for g in Group.objects.all()]
    