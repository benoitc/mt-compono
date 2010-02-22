# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.


from couchdbkit.ext.django import loading
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context


from goldorak.apps.pages.models import Page

                                      
def page_handler(request, path=None):
    page = Page.from_path(path)
    if page is None:
        return create_page(request)
    return show_page(request, page)
    
def create_page(request):
    return render_to_response("pages/create_page.html", {
        "path": request.path
    }, context_instance=RequestContext(request))
    
def show_page(request, page):
    print page
    pass