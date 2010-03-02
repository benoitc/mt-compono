# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.
import os

from django.conf import settings
from django.conf.urls.defaults import patterns, url

COMPONO_MEDIA_ROOT = getattr(settings, 'COMPONO_MEDIA_ROOT', 
                        os.path.join(os.path.dirname(__file__), 'media'))
COMPONO_MEDIA_URL = getattr(settings, 'COMPONO_MEDIA_URL', '/media/compono')

print COMPONO_MEDIA_URL
print COMPONO_MEDIA_ROOT

urlpatterns = patterns('compono.views',
    url(r'^types', 'types', name='types'),
    url(r'^type/(?P<name>.*)$', 'type', name='types'),
    url(r'^type/(?P<name>.*)/pages$', 'page_by_types', name='page_by_types'),
    url(r'^%s/(?P<path>.*)$' % COMPONO_MEDIA_URL, 'django.views.static.serve', 
            {'document_root': COMPONO_MEDIA_ROOT}),
)
    
urlpatterns += patterns('compono.views',
    url(r'^(?P<path>.*)$', 'page_handler', name='page_handler'),
)