/* This file is part of compono released under the Apache 2 license. 
 See the NOTICE for more information. */
 
function(doc) {
  if (doc.doc_type == "page") {
    emit(doc.ctype, null);
  }
  
}