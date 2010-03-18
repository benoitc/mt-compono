# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

import base64

from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.html import escape

try:
    import simplejson as json
except ImportError:
    from django.utils import simplejson as json

MTCOMPONO_MEDIA_URL = getattr(settings, 'MTCOMPONO_MEDIA_URL', 
                        '/media/mtcompono')


class TemplateWidget(forms.Widget):
    needs_multipart_form = True
    
    class Media:
        js = (MTCOMPONO_MEDIA_URL + "/js/jquery.base64.js",
              MTCOMPONO_MEDIA_URL + "/js/codemirror/codemirror.js",
              MTCOMPONO_MEDIA_URL + "/js/goldorak.page_template.js")
    
    def render(self, name, value, attrs=None):
        if value is None: value = {}
        if "id" in attrs:
            del attrs['id']
            
        values = dict([(k, escape(value[k])) for k in value.keys()])
        html = [
            '<script>var TEMPLATES=%s;</script>' % json.dumps(values, indent=2),
            '<select id="editTemplate">',
            '<option value="-">Choose an existing template to edit</option>'
        ]
        for k in value.keys():
            html.append('<option value="%(key)s">%(key)s</option>' % {"key": k})
        
        html.append('</select>')
        html.append('<a href="#" id="createTemplate">Create a new template</a>')
        html.append('<textarea id="tpl"%s></textarea>' % flatatt(attrs))
        
        return mark_safe(u'\n'.join(html))
        
    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        d =  data.get(name, None)
        if not d:
            return {}
        if isinstance(d, dict):
            return d
        return json.loads(base64.b64decode(d))