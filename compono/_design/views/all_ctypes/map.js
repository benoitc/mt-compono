function(doc) {
  if (doc.doc_type == "ctype") {
    emit(doc._id, null);
  }
}