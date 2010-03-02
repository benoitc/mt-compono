# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('goldorak.apps.pages.views',
    url(r'^types', 'types', name='types'),
    url(r'^type/(?P<name>.*)$', 'type', name='types'),
    url(r'^type/(?P<name>.*)/pages$', 'page_by_types', name='page_by_types'),
    url(r'^(?P<path>.*)$', 'page_handler', name='page_handler'),
)