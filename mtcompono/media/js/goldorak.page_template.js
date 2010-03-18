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
  
  var current_template = "";
  
  $("#editTemplate").change(function(e) {
    if (current_template != "") {
      TEMPLATES[current_template] = escapeHTML(cde.getCode());
    }
    
    var tname = $("#editTemplate").val();
    current_template = tname;
    cde.setCode(unescaperHTML(TEMPLATES[tname]));
  })
  
  $("#editTemplate").parents("form").submit(function() {
    if (current_template != "") {
      TEMPLATES[current_template] = escapeHTML(cde.getCode());
    }
    
    var templates_str = $.base64.encode(JSON.stringify(TEMPLATES));
    
    $(this).append('<input type="hidden" name="templates" value="'+
      templates_str + '">');
    
  });
  
  
});