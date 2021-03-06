# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.
import os

from django.conf import settings
from django.conf.urls.defaults import patterns, url

from mtcompono.views.type import all_types, edit_type, pages_by_type
from mtcompono.views.page import page_handler, new_document

MTCOMPONO_MEDIA_ROOT = getattr(settings, 'MTCOMPONO_MEDIA_ROOT', 
                        os.path.join(os.path.dirname(__file__), 'media'))
MTCOMPONO_MEDIA_URL = getattr(settings, 'MTCOMPONO_MEDIA_URL', 
                        'media/mtcompono')


if MTCOMPONO_MEDIA_URL.startswith('/'):
    MTCOMPONO_MEDIA_URL = MTCOMPONO_MEDIA_URL[1:]

if settings.APPEND_SLASH:
    unknown = url(r'^(?P<path>.*)/$', page_handler, name='page_handler')
else:
    unknown = url(r'^(?P<path>.*)$', page_handler, name='page_handler')

urlpatterns = patterns('',
    url(r'^document', new_document, name='new_document'),
    url(r'^types$', all_types, name='all_types'),
    url(r'^type/(?P<typeid>.*)$', edit_type, name='edit_type'),
    url(r'^type$', edit_type, name='edit_type'),

    
    (r'^%s/(?P<path>.*)$' % MTCOMPONO_MEDIA_URL, 'django.views.static.serve', 
              {'document_root': MTCOMPONO_MEDIA_ROOT})
)