# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('goldorak.apps.pages.views',
    url(r'^(?P<path>.*)$', 'page_handler', name='page_handler'),
)