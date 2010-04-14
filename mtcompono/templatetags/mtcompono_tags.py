# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django.conf import Settings
from django.template import Library, Node, Template, TemplateSyntaxError
from mtcompono.models import Type

register = Library()

class ListTypeNode(Node):
    
    def __init__(self, type_name):
        self.type_name = type_name

    def render(self, context):
        t = Type.by_name(self.type_name)
        if not t:
            if settings.DEBUG:
                return "[%s don't exist]" % self.type_name
            else:
                return ''
            
        items = t.get_items()
        output = ''
        try:
            tpl = Template(t.templates['list'])
            context.update({"items": items})
            output = tpl.render(context)
        except TemplateSyntaxError, e:
            if settings.DEBUG:
                return "[Included list had syntax error: %s]" % e
            else:
                return ''
        return output
        

def list_type(parser, token):
    bits = token.contents.split()
    if len(bits) < 2:
        raise TemplateSyntaxError("'list_type' tag takes one argument: the type"
                                  " name to list")
                                  
    return ListTypeNode(bits[1])
list_type = register.tag(list_type)
    
    