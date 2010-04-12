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

from mtcompono.forms import CreatePageType, EditType
from mtcompono.models import Page
from mtcompono.permissions import can_create, can_edit


from mtcompono.models import Page, Type


def page_handler(request, path=None):
    """ main page handler """
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
        fcreate = CreatePageType(request.POST)
        if fcreate.is_valid():
            path = fcreate.cleaned_data['path']
            if path.endswith('/'): path = path[:-1]
            pname = fcreate.cleaned_data['name']
            p = Page({
                "name": pname,
                "urls": [path],
                "editors": fcreate.cleaned_data['editors'],
                "need_edit": True
            })
            p.save()
            if  fcreate.cleaned_data['page_type'] == "type":
                redirect_path = reverse('edit_type', kwargs=dict(name=pname,
                                                        path=path))

            else:
                redirect_path = "%s?edit=1" % reverse('page_handler', 
                                                    kwargs=dict(path=path))
            return HttpResponseRedirect(redirect_path)
    else:
        fcreate = CreatePageType(initial=dict(path=path))
    
    return render_to_response("pages/create_page.html", {
        "path": request.path,
        "f": fcreate
    }, context_instance=RequestContext(request))
    
def edit_page(request, page):
    if page.doc_type == "page":
        return edit_cnt(request, page)
    else:
        return edit_ctx(request, page)
        
def edit_cnt(request, page):
    raise Http404()

def edit_ctx(requuest, page):
    ctx = CtxPage.from_page(page)
    if request.method == "POST":
        fctx = EditContext(request.POST)
        if fctx.is_valid():
            ctx.template = fctx.cleaned_data['template']
            ctx.save()
    else:
        
        fctx = EditContext(initial={'template': ctx.template })

    return render_to_response("pages/edit_context.html", {
        
    }, context_instance=RequestContext(request))


def show_page(request, page):
    return render_to_response("pages/create_page.html", {
        "path": request.path
    }, context_instance=RequestContext(request))