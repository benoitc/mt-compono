# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from __future__ import with_statement

import os
import urllib

from django.conf import settings
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponseRedirect, HttpResponse, \
HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse


from mtcompono.forms import EditType
from mtcompono.permissions import can_create, can_edit

from mtcompono.models import Type

try:
    import simplejson as json
except ImportError:
    import json

from couchdbkit import ResourceConflict

DEFAULT_TEMPLATE = os.path.join(os.path.dirname(__file__), '..', 'templates',
                                'mtcompono', "default.html")

def all_types(request):
    """ list all types """
    
    if not can_create(request.user):
        return HttpResponseForbidden()
    
    types = Type.all()
    return render_to_response("types/types.html", {
        "types": types
    }, context_instance=RequestContext(request))
    
def edit_type(request, typeid=None):
    """ Edit a page type """
    
    if not can_create(request.user):
        return HttpResponseForbidden()
    
    if request.POST:
        data = json.loads(request.raw_post_data)
        old_t = Type.by_name(data['name'])
        
        if old_t and old_t._id != data.get("_id"):
            return HttpResponse(content=json.dumps({"error": True,
                    "reason": "conflict - type already created"}),
                    status="409")
                    
        typeid = data.pop('_id', "")
        typerev = data.pop('_rev', "")
        
        t = Type(**data)
        
        if typeid: t._doc['_id'] = typeid
        if typerev: t._doc['_rev'] = typerev
        
        try:
            t.save()
        except ResourceConflict, e:
            return HttpResponse(content=json.dumps({"error": True,
                    "reason": str(e)}), status="409")
        return HttpResponse(content=json.dumps({"ok": True, "id": t._id, 
            "rev": t._rev}), content_type="application/json")
    
    doc = {}
    if typeid and typeid is not None:
        doc = Type.get(typeid).to_json()
        
    return render_to_response("types/type.html", {
         "doc": json.dumps(doc),
         "editors": Group.objects.all()
    }, context_instance=RequestContext(request))
                
def pages_by_type(request, name):
    raise Http404()    