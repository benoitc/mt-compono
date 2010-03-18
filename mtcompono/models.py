# -*- coding: utf-8 -*-
#
# This file is part of compono released under the Apache 2 license. 
# See the NOTICE for more information.

from datetime import datetime
import urllib

from couchdbkit.ext.django.schema import Document, StringProperty, \
DateTimeProperty, StringListProperty, BooleanProperty, DictProperty

try:
    import simplejson as json
except ImportError:
    from django.utils import simplejson as json
    
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
    templates = DictProperty()
    
    groups = StringListProperty()
    ctype = StringProperty()
    urls = StringListProperty()
    
    doc_type = "ctype"
    
    @classmethod
    def all(cls):
        return cls.view('mtcompono/all_types', include_docs=True)
        
    @classmethod
    def by_name(cls, tname):
        res = cls.view('mtcompono/ctypes_by_name', key=tname, 
                    include_docs=True).first()
        return res
        

class Page(DocRev):
    """ a generic mapper for a page """    
    
    urls = StringListProperty()
    need_edit = BooleanProperty(default=True)
    draft = BooleanProperty(default=False)
    
   
    @classmethod    
    def from_path(cls, path):
        key = path.split('/')
        res = cls.view("mtcompono/from_path", key=key, include_docs=True).first()
        return res
        
    @classmethod
    def from_page(cls, page_instance):
        """ create a page instance from another """
        obj = cls()
        obj._doc = page_instance._doc.copy()
        return obj
        
class CntPage(Page):
    """ a content page """
        
    doc_type = "page"       

    @classmethod
    def by_type(cls, tname):
        return cls.view("mtcompono/page_by_ctype", key=tname, 
                    include_docs=True).first()
                    
    @classmethod
    def from_path():
        key = path.split('/')
        res = cls.view("mtcompono/cnt_from_path", key=key, 
                    include_docs=True).first()
        return res
    
class Context(Page):
    """ a context page """
    
    doc_type = "context"
    
    @classmethod
    def from_path(cls, path):
        key = path.split('/')
        res = cls.view("mtcompono/ctx_from_path", key=key, 
                    include_docs=True).first()
        return res