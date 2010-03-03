# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from datetime import datetime
from couchdbkit.ext.django.schema import Document, StringProperty, \
DateTimeProperty, StringListProperty, BooleanProperty

class Page(Document):
    title = StringProperty()
    page_type = StringProperty(default="page")
    groups = StringListProperty()
    ctype = StringProperty()
    urls = StringListProperty()
    need_edit = BooleanProperty(default=True)
    draft = BooleanProperty(default=False)
    created = DateTimeProperty()
    updated = DateTimeProperty(default=datetime.utcnow)

    doc_type = "page"
    
    def save(self, **params):
        if not self._rev:
            self.created = datetime.utcnow()    
        super(Page, self).save(**params)
        
        # add a revision
        attachment_name = "rev_%s" % self._doc['updated']
        self.put_attachment(attachment_name, self.to_json(), 
                        content_type="application/json")
    
    @classmethod    
    def from_path(cls, path):
        key = path.split('/')
        res = cls.view("compono/from_path", key=key, include_docs=True).first()
        return res
        
    @classmethod
    def by_type(cls, tname):
        return cls.view("compono/page_by_ctype", key=tname, 
                    include_docs=True).first()
        

class Type(Document):
    title = StringProperty()
    description = StringProperty()
    
    doc_type = "ctype"
    
    @classmethod
    def all(cls):
        return cls.view('compono/all_types', include_docs=True)
        
    @classmethod
    def by_name(self, tname):
        return cls.view('compono/ctype_by_name', include_docs=True).first()