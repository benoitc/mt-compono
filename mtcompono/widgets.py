# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe

try:
    import simplejson as json
except ImportError:
    from django.utils import simplejson as json

MTCOMPONO_MEDIA_URL = getattr(settings, 'MTCOMPONO_MEDIA_URL', 
                        '/media/mtcompono')


class TemplateWidget(forms.Widget):
    needs_multipart_form = True
    
    class Media:
        js = (MTCOMPONO_MEDIA_URL + "js/codemirror/codemirror.js",
              MTCOMPONO_MEDIA_URL + "js/goldorak.page_template.js")
    
    def render(self, name, value, attrs=None):
        if value is None: value = {}
        
        html = []
        html.append('<script>var templates=%s;</script>' % json.dumps(value))
        html.append('<select name="tname">')
        for k in value.keys():
            html.append('<option value="%(key)s">%(key)s</option>' % {"key": k})
        
        html.append('</select>')
        html.append('<textarea id="tpl"></textarea>')
        
        return mark_safe(u'\n'.join(html))