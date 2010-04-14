# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from __future__ import with_statement

import os
import urllib

from django.conf import settings
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse

from mtcompono.forms import CreatePageType, EditContent, EditContext
from mtcompono.models import Page, ContextPage
from mtcompono.permissions import can_create, can_edit


from mtcompono.models import Page, Type
from mtcompono.util import render_template

from couchdbkit import ResourceNotFound

def page_handler(request, path=None):
    """ main page handler """
    if path == "/" or not path:
        path = "/"
    elif path.endswith('/'): 
        path = path[:-1]
        
    page = Page.from_path(path)
    if page is None:
        if can_create(request.user):
            return create_page(request, path)
        raise Http404
        
    if request.REQUEST.get('edit') and can_edit(request.user, page):
        return edit_page(request, page)
    elif request.POST and can_edit(request.user, page):
        return edit_page(request, page)
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
            if path != "/" and path.endswith('/'):
                # shouldn't happen but who knows 
                path = path[:-1]
                
            action = fcreate.cleaned_data['page_type']
            if action == "type":
                redirect_path = "%s?r=%s" % (reverse("edit_type"), path)
                return HttpResponseRedirect(redirect_path)
            elif action == "context":
                page = ContextPage(urls=[path], author=request.user.username)
                page.save()
                return edit_context(request, page, create=True)
            elif action != "--":
                page = Page(ctype=action, urls=[path], 
                            author=request.user.username)
                page.save()
                
                return edit_page(request, page, create=True)
    elif request.GET.get('edit', '') and request.GET.get('type', ''):
        page = Page(ctype=request.GET.get('type'), urls=[path], 
                author=request.user.username)
        page.save()
        return edit_page(request, page, create=True)
        
    fcreate = CreatePageType(initial=dict(path=path))
    
    return render_to_response("pages/create_page.html", {
        "path": request.path,
        "f": fcreate
    }, context_instance=RequestContext(request))
    
def edit_page(request, page, create=False):
    if page.doc_type == "page":
        return edit_content(request, page, create=create)
    else:
        return edit_context(request, page, create=create)
        
def edit_content(request, page, create=False):
    try:
        t = Type.get(page.ctype)
    except ResourceNotFound:
        raise Http404()
    
    if request.POST and not create:
        f = EditContent(request.POST, type_instance=t, document_instance=page)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(request.path)
    else:
        f = EditContent(type_instance=t, document_instance=page)
    return render_to_response("pages/page.html", {
        "f": f,
        "path": request.path
    }, context_instance=RequestContext(request))

def edit_context(request, page, create=False):
    if request.method == "POST" and not create:
        fctx = EditContext(request.POST)
        if fctx.is_valid():
            page.body = fctx.cleaned_data['body']
            page.editors = fctx.cleaned_data['editors']
            page.title = fctx.cleaned_data['title']
            page.save()
            return HttpResponseRedirect(request.path)
    else:
        fctx = EditContext(initial={
            "body": page.body,
            "editors": page.editors,
            "title": page.title
        })

    return render_to_response("pages/context.html", {
        "f": fctx,
        "path": request.path
    }, context_instance=RequestContext(request))


def show_page(request, page):
    if page.doc_type == "context":
        content = render_template(page.body,
                        context_instance=RequestContext(request))
        return HttpResponse(content)
    else:
        try:
            t = Type.get(page.ctype)
        except ResourceNotFound:
            raise Http404()
        content = render_template(t.templates['show'], {
            "doc": page
        }, context_instance=RequestContext(request))
        return HttpResponse(content)
    raise Http404()