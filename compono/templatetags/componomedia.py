# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django.template import Library
from django.utils.encoding import iri_to_uri

register = Library()


def compono_media_url():
    """
    Returns the string contained in the setting COMPONO_MEDIA_URL.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    
    COMPONO_MEDIA_URL = getattr(settings, 'COMPONO_MEDIA_URL', 
                            '/media/compono')
                                                  
    return iri_to_uri(COMPONO_MEDIA_URL)
compono_media_url = register.simple_tag(compono_media_url)