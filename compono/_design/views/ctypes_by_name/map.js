function(doc) {
  if (doc.doc_type == "ctype") {
    emit(doc.name, null);
  }
}