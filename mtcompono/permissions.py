# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.


def can_create(user):
    if not user.is_authenticated():
        return False
    if user.groups.filter(name="administrateurs").count() > 0:
        return True
    return False
    
def can_edit(user, page):
    if not user.is_authenticated():
        return False
    if not can_create(user):    
        for g in user.groups.all():
            if g.name:
                return True
                
        return False
    else:
        return True