# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from datetime import datetime
from couchdbkit.ext.django.schema import Document, StringProperty, \
DateTimeProperty, StringListProperty

class Page(Document):
    title = StringProperty()
    page_type = StringProperty(default="page")
    urls = StringListProperty()
    created = DateTimeProperty()
    updated = DateTimeProperty(default=datetime.utcnow)

    doc_type = "page"
    
    def save(self, **params):
        if not self._rev:
            self.created = datetime.utcnow()
        super(Page, document).save(**params)
    
    @classmethod    
    def from_path(self, path):
        key = path.split('/')
        res = self.view("pages/from_path", key=key, include_doc=True).first()
        if not res:
            return None
        return res['value']
        

        