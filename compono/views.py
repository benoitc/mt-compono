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


from compono.forms import CreatePage, EditType
from compono.models import Page, Type
from compono.permissions import can_create, can_edit

DEFAULT_TEMPLATE = os.path.join(os.path.dirname(__file__), 'templates',
                                'compono', "default.html")

def page_types(request):
    types = Type.all()
    return render_to_response("types/types.html", {
        "types": types
    }, context_instance=RequestContext(request))


def edit_ctx(request, name):
    raise Http404()

def edit_type(request, name):
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

def page_by_type(request, tname):
    pages = Page.by_type(tname)
    return render_to_response("types/pages.html", {
        "pages": pages
    }, context_instance=RequestContext(request))
                
def page_handler(request, path=None):
    if path.endswith('/'): path = path[:-1]
    page = Page.from_path(path)
    if page is None:
        if can_create(request.user):
            return create_page(request, path)
        raise Http404
        
    if request.GET.get('edit') and can_edit(request.user, page):
        return edit_page(request, page)
    elif page.need_edit:
        if can_edit(request.user, page):
            return edit_page(request, page)
        else:
            raise Http404
    elif page.draft:
        if request.user.is_authenticated():
            return show_page(request, page)
        else:
            raise Http404
    else:
        return show_page(request, page)
    
def create_page(request, path):
    if request.method == "POST":
        fcreate = CreatePage(request.POST)
        if fcreate.is_valid():
            path = fcreate.cleaned_data['path']
            if path.endswith('/'): path = path[:-1]
            pname = fcreate.cleaned_data['name']
            t = Type({
                "name": pname,
                "urls": [path],
                "editors": fcreate.cleaned_data['editors'],
                "need_edit": True
            })
            t.save()
            if  fcreate.cleaned_data['page_type'] == "type":
                redirect_path = reverse('edit_type', kwargs={"name":pname})
            else:
                redirect_path = reverse('edit_ctx', kwargs={"name":pname})
            return HttpResponseRedirect(redirect_path)
    else:
        fcreate = CreatePage(initial=dict(path=path))
    
    return render_to_response("pages/create_page.html", {
        "path": request.path,
        "f": fcreate
    }, context_instance=RequestContext(request))
    
def edit_page(request, page):
    raise Http404()

def show_page(request, page):
    return render_to_response("pages/create_page.html", {
        "path": request.path
    }, context_instance=RequestContext(request))
