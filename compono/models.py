# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from datetime import datetime
import urllib

from couchdbkit.ext.django.schema import Document, StringProperty, \
DateTimeProperty, StringListProperty, BooleanProperty

try:
    import simplejson as json
except ImportError:
    import json
    
class DocRev(Document):
    """ document with revisions """
    created = DateTimeProperty()
    updated = DateTimeProperty()
    
    def save(self, **params):
        if not self._rev:
            self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        super(DocRev, self).save(**params)
        # add a revision
        attachment_name = "rev_%s" % self._doc['updated']
        self.put_attachment(json.dumps(self.to_json()), attachment_name, 
                        content_type="application/json")
        

class Type(DocRev):
    name = StringProperty()
    title = StringProperty()
    body = StringProperty()
    template = StringProperty()
    page_type = StringProperty(default="page")
    groups = StringListProperty()
    ctype = StringProperty()
    urls = StringListProperty()
    need_edit = BooleanProperty(default=True)
    draft = BooleanProperty(default=False)
    
    doc_type = "ctype"
    
    @classmethod
    def all(cls):
        return cls.view('compono/all_types', include_docs=True)
        
    @classmethod
    def by_name(cls, tname):
        res = cls.view('compono/ctype_by_name', key=tname, 
                    include_docs=True).first()
        print res
        return res
        

class Page(DocRev):
    title = StringProperty()
    body = StringProperty()
    
    doc_type = "page"
    
    @classmethod    
    def from_path(cls, path):
        key = path.split('/')
        res = cls.view("compono/from_path", key=key, include_docs=True).first()
        return res
        
    @classmethod
    def by_type(cls, tname):
        return cls.view("compono/page_by_ctype", key=tname, 
                    include_docs=True).first()
    
   