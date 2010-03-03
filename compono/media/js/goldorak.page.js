/* This file is part of compono released under the Apache 2 license. 
 See the NOTICE for more information. */

(function($) {

  var template_path = COMPONO_MEDIA_URL + '/templates/';
  
  var config = {
    toolbar:
    [
    ['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 
    'Unlink'], 
    ['UIColor']
    ]
  };
  
  
  var field_types = [
    {
      id: "t",
      label: "Text input",
      tpl: '<input type="text" name="{{ name }}" id="{{ name }}">'
    },
    {
      id: "ta",
      label: "Long Text input",
      tpl: '<br><textarea name="{{ name }}" id="{{ name }}" class="resize">'
            + '</textarea>'
    }
  ];
  
  var new_input = '<p class="custom"><input type="text" name="{{lname}}" id="{{lname}}"'
  +' value="{{ label }}"> {{>tpl}}<a class="delete" href="#">delete</a></p>';

  $.goldorak = $.goldorak || {};
  $.extend($.goldorak, {

    editor: function(el) {
      $(el).ckeditor(config);
    },

    createPage: function() {
      var page = this;
      var nb_fields = 0;
      var dt = {};
      
      for (i=0; i<field_types.length; i++) {
        var field = field_types[i];
        dt[field.id] = field;
        
        $('<li><a href="#" id="' + field.id +'">'+field.label+'</a></li>')
        .click(function(e, el) {
          e.preventDefault();
          nb_fields += 1;
          var id = $('a', this).attr('id');
          var f = dt[id];
          var label = f.label + " " + nb_fields;
          var fname = f.id + "_" + nb_fields;          
         
          var h = Mustache.to_html(new_input, {
            lname: "lcustom -" + fname,
            label: label,
            tpl: {
              name: "custom -" + fname
            }
          }, { tpl: f.tpl});
          
          
          var inp = $(h);
          $('a.delete', inp).click(function(e) {
            e.preventDefault();
            $(this).parent().remove()
            return false;
          }).appendTo(inp);
          
          $("#custom_fields").append(inp);
        })
        .appendTo('#fieldsTypes');
        
      }
      

    }
  });
})(jQuery);