$(function() {
  new CodeMirror.fromTextArea("tpl",  {
        parserfile: "parsexml.js",
        stylesheet: MTCOMPONO_MEDIA_URL +"/css/xmlcolors.css",
        path: MTCOMPONO_MEDIA_URL + "/js/codemirror/",
        height: "450px"

  });
});