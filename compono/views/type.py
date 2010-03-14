# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from __future__ import with_statement

import os
import urllib

from django.conf import settings
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse


from compono.forms import EditType
from compono.permissions import can_create, can_edit

from compono.models import Type


DEFAULT_TEMPLATE = os.path.join(os.path.dirname(__file__), '..', 'templates',
                                'compono', "default.html")

def all_types(request):
    """ list all types """
    
    types = Type.all()
    return render_to_response("types/types.html", {
        "types": types
    }, context_instance=RequestContext(request))
    
def edit_type(request, name):
    """ Edit a page type """
    
    t = Type.by_name(name)
    msg = None
    if request.POST:
        fedit = EditType(request.POST, auto_id=False, instance=t)
        if fedit.is_valid():
            t = fedit.save()
            msg = "Page saved"
    else:
        initial = {}
        if not t.template:
            default = getattr(settings, 'COMPONO_DEFAULT_TEMPLATE', 
                            DEFAULT_TEMPLATE)

            with open(default, 'r') as f:
                initial.update({'template':f.read()})
        fedit = EditType(initial=initial, auto_id=False, instance=t)

    return render_to_response("types/type.html", {
        "f": fedit,
        "msg": msg
    }, context_instance=RequestContext(request))
    
    return render_to_response("types/type.html", {
        "t": types
    }, context_instance=RequestContext(request))
    

def page_by_type(request, name):
    raise Http404()    