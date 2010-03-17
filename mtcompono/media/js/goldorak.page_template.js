$(function() {
  var cde = new CodeMirror.fromTextArea("tpl",  {
        parserfile: "parsexml.js",
        stylesheet: MTCOMPONO_MEDIA_URL +"/css/xmlcolors.css",
        path: MTCOMPONO_MEDIA_URL + "/js/codemirror/",
        height: "450px"

  });
  
  function escapeHTML(st) {
    return(
      st && st.replace(/&/g,'&amp;').
      replace(/>/g,'&gt;').
      replace(/</g,'&lt;').
      replace(/"/g,'&quot;')
    );
  };
  
  function unescaperHTML(s) {
    return (
      s && s.replace(/&#(\d+);/g, function(wm, pmatch){
        return String.fromCharCode(+pmatch);
      }).replace(/&amp;/g, '&').
      replace(/&gt;/g, '>').
      replace(/&lt;/g, '<').
      replace(/&quot;/g, '"')
    );
    
  }
  
  $("#editTemplate").change(function(e) {
    var tname = $("#editTemplate").val();
    cde.setCode(unescaperHTML(TEMPLATES[tname]));
  })
  
});