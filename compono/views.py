# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.


from couchdbkit.ext.django import loading
from django.conf import settings
from django.contrib.auth.models import Group
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context


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
    page = Page.from_path(path)
    if page is None:
        user = getattr(request, 'user')
        if user and user.is_authenticated():
            if user.groups.filter(name="administrateurs").count() > 0:
                return create_page(request)
        raise Http404
    return show_page(request, page)
    
def create_page(request):
    groups = Group.objects.all()
    
    return render_to_response("pages/create_page.html", {
        "path": request.path,
        'groups': Group.objects.all()
    }, context_instance=RequestContext(request))
    
def show_page(request, page):
    return render_to_response("pages/create_page.html", {
        "path": request.path
    }, context_instance=RequestContext(request))
