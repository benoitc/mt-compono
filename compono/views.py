# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django.conf import settings
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse


from compono.forms import CreatePage
from compono.models import Page, Type

def page_types(request):
    types = Type.all()
    return render_to_response("types/types.html", {
        "types": types
    }, context_instance=RequestContext(request))


def page_type(request, name):
    t = Type.by_name(name)
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
        
        if request.user.is_authenticated():
            if user.groups.filter(name="administrateurs").count() > 0:
                return create_page(request, path)
        raise Http404
    if request.GET.get('edit') == "1" and request.user.is_authenticated():
        print "ici"
        return edit_page(request, page)
    return show_page(request, page)
    
def create_page(request, path):
    if request.method == "POST":
        fcreate = CreatePage(request.POST)
        if fcreate.is_valid():
            path = fcreate.cleaned_data['path']
            if path.endswith('/'): path = path[:-1]
            page = Page({
                "urls": [path],
                "editors": fcreate.cleaned_data['editors'],
                "page_type": fcreate.cleaned_data['page_type']
            })
            page.save()
            redirect_path = "%s?edit=1" % reverse('page_handler', 
                                                kwargs={"path":path})
            return HttpResponseRedirect(redirect_path)
    else:
        fcreate = CreatePage(initial=dict(path=path))
    
    return render_to_response("pages/create_page.html", {
        "path": request.path,
        "f": fcreate
    }, context_instance=RequestContext(request))
    
def edit_page(request, page):
    return render_to_response("pages/edit_page.html", {
    }, context_instance=RequestContext(request))

def show_page(request, page):
    return render_to_response("pages/create_page.html", {
        "path": request.path
    }, context_instance=RequestContext(request))
