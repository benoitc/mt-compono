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

  $.goldorak = $.goldorak || {};
  $.extend($.goldorak, {

    editor: function(el) {
      $(el).ckeditor(config);
    },

    createPage: function() {
      var page = this;
      var app = $.sammy(function() {

        this.element_selector = "#create";
        this.use(Sammy.Mustache, 'html');


        this.get("#/create/content", function(ctx) {
          ctx.app.swap('');
          this.partial(template_path + "create_content.html", { 
            page_type: "content" }, function(response) {
              $("#create").html(response);
              $.goldorak.editor("#content");
            });

        });

        this.get("#/create/context", function(ctx) {
          ctx.app.swap('');
          this.partialtemplate_path + ("create_context.html", 
          { page_type: "context" }, function(response) {
            $("#create").html(response);
          });

        });

        this.post("#/", function(ctx) {
          var page_type = this.params['page_type'];
          this.redirect("#/create/"+page_type);
        })

        this.get("#/", function(ctx) {
          ctx.app.swap('');
          this.partial(template_path + "create_page.html", 
          function(response) {
            $("#create").html(response);
          });

        });

      });

      $(function() {
        app.run("#/");
      });

    }
  });
})(jQuery);