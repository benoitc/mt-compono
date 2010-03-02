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
    ctype = StringProperty()
    urls = StringListProperty()
    created = DateTimeProperty()
    updated = DateTimeProperty(default=datetime.utcnow)

    doc_type = "page"
    
    def save(self, **params):
        if not self._rev:
            self.created = datetime.utcnow()
        super(Page, document).save(**params)
    
    @classmethod    
    def from_path(cls, path):
        key = path.split('/')
        res = cls.view("compono/from_path", key=key, include_doc=True).first()
        return res
        
    @classmethod
    def by_type(cls, tname):
        return cls.view("compono/page_by_ctype", key=tname, 
                    include_doc=True).first()
        

class Type(Document):
    title = StringProperty()
    description = StringProperty()
    
    doc_type = "ctype"
    
    @classmethod
    def all(cls):
        return cls.view('compono/all_types', include_doc=True)
        
    @classmethod
    def by_name(self, tname):
        return cls.view('compono/ctype_by_name', include_doc=True).first()