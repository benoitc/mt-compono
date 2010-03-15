# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django.template import Library
from django.utils.encoding import iri_to_uri

register = Library()


def mtcompono_media_url():
    """
    Returns the string contained in the setting MTCOMPONO_MEDIA_URL.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    
    MTCOMPONO_MEDIA_URL = getattr(settings, 'MTCOMPONO_MEDIA_URL', 
                            '/media/mtcompono')
                                                  
    return iri_to_uri(MTCOMPONO_MEDIA_URL)
mtcompono_media_url = register.simple_tag(mtcompono_media_url)