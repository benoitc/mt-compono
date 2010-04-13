# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.


from django import template

def render_template(template_str, dictionary=None, context_instance=None):
    dictionary = dictionary or {}
    t = template.Template(template_str)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = template.Context(dictionary)
    return t.render(context_instance)
    