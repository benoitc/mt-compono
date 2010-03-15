/* This file is part of compono released under the Apache 2 license. 
 See the NOTICE for more information. */
 
function(doc) {
  if (doc.doc_type == "ctx") {
    for(var i=0; i < doc.urls.length; i++) {
        path = doc.urls[i].split("/");
        emit(path, null);
    }
  }
}