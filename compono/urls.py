# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.
import os

from django.conf import settings
from django.conf.urls.defaults import patterns, url

from compono.views import page_types, page_type, page_by_type, page_handler

COMPONO_MEDIA_ROOT = getattr(settings, 'COMPONO_MEDIA_ROOT', 
                        os.path.join(os.path.dirname(__file__), 'media'))
COMPONO_MEDIA_URL = getattr(settings, 'COMPONO_MEDIA_URL', 
                        'media/compono')


if COMPONO_MEDIA_URL.startswith('/'):
    COMPONO_MEDIA_URL = COMPONO_MEDIA_URL[1:]

if settings.APPEND_SLASH:
    r = url(r'^(?P<path>.*)/$', page_handler, name='page_handler')
else:
    r = url(r'^(?P<path>.*)$', page_handler, name='page_handler')

urlpatterns = patterns('',
    url(r'^types', page_types, name='page_types'),
    url(r'^type/(?P<name>.*)$', page_type, name='page_types'),
    url(r'^type/(?P<name>.*)/pages$', page_by_type, name='page_by_types'),
    (r'^%s/(?P<path>.*)$' % COMPONO_MEDIA_URL, 'django.views.static.serve', 
              {'document_root': COMPONO_MEDIA_ROOT}),
    r,
)