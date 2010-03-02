function(doc) {
  if (doc.doc_type == "page") {
    emit(doc.ctype, null);
  }
  
}