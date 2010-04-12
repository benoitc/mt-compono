/* This file is part of compono released under the Apache 2 license. 
 See the NOTICE for more information. */

(function($) {

  var template_path = MTCOMPONO_MEDIA_URL + '/templates/';
  
  var new_input = '<div class="custom"><input type="text" name="{{lname}}"'
  +' id="{{lname}}" value="{{ label }}">{{>tpl}}<a class="delete" href="#">'
  +'delete</a></p>';
  
  function Type(options) {
    this.options = options;
    this.property_path = options.path + "properties/";
    
    this.available_properties = {};
    this.nb_fields = 0;
    
    this._templates = {
      "list": "",
      "show": ""
    };
    
    this._properties = {}
    this._fields = {};
    this.current_template = "";
    this.cde = null;
    this._id = "";
    this._rev = "";
    
    var self = this;
    
    this.add_widget = function (prop) {
      var tpl_path = self.property_path + prop.name + ".html";

      var label = prop.label;
      var fname = prop.id;

      $.compono.load(tpl_path, function(html) {
        var h = Mustache.to_html(new_input, {
          lname: "lprop_" + fname,
          label: label,
          tpl: {
            name: "prop_" + fname
          }
        }, {
          tpl: html
        });

        var inp = $(h);
        $('a.delete', inp).click(function(e) {
          e.preventDefault();
          $(this).parent().remove()
          return false;
        });
        $(".date", inp).datepicker();

        $("#properties").append(inp);

        $.compono.editor(".txt");
      });
    }
    
    this.add_type = function(e, el) {
      e.preventDefault();
      self.nb_fields += 1;
      var id = $('a', this).attr('id');
      var prop = self.available_properties[id];
      prop.id = prop.id + "_" + self.nb_fields;
      prop.label = prop.label + " " + self.nb_fields;
      self.add_widget(prop);
      
    }
    
    this.saveType = function(e) {
      e.preventDefault();
      var aform = $(this).serializeArray();
      
      var ojson = {};
      var aproperties = [];
      var templates = {};
      var nb_properties = 0;
      var properties = self._properties;
      
      $.each(aform, function() {
        var el = $(this);
        var name = el.attr('name');
        var field_type = el.attr('type');
        if (name.startsWith("lprop_")) {
          var fid = name.substr(6);
          var type = fid.split("_")[0];            
          var prop = self.available_properties[type];            
          if (!ojson[fid]) {
            nb_properties += 1;
            o = {
              "id": fid,
              "label": el.attr("value"),
              "type": prop['propertyName'],
              "name": prop['name']
            }
            
            ojson[fid] = o;
            aproperties.push(o)
          }
        } else if (name.startsWith("tpl_")) {
          tname = name.substr(4);
          templates[tname] = el.attr("value");
        } else if (!name.startsWith("prop_") && !name.startsWith("csrf") &&
                  field_type != "submit" &&
                  (name != "templates") && (name != "tpl")) {
          properties[name] = el.attr("value");
          if (self._id) properties['_id'] = self._id;
          if (self._rev) properties['_rev'] = self._rev;
        }
      });
      
      if (nb_properties == 0) {
        alert("No properties defined.")
      } else if (!properties["name"]) {
        alert("You should defined name of the type.");
      } else {
        properties["props"] = aproperties;
        properties["templates"] = templates;
                
        $.ajax({
          type: "POST",
          url: $(this).attr("action"),
          data: JSON.stringify(properties),
          dataType: "json",
          success: function(data) {
            self._id = data.id;
            self._rev = data.rev;
          }
        });
      }
      return false;
    
    };
    
    this.changeTemplate = function(e) {
      $("#tpl_"+ self.current_template).val(self.cde.getCode());
      var tname = $("#templates").val();
      if (tname != self.current_template) {
        self.current_template = tname;
        self.cde.setCode($("#tpl_" + tname).val());
      }
    };
    
    function init_templates(options) {
      self.current_template = "show";
      $("#tpl").val($("#tpl_show").val())
      
      self.cde = new CodeMirror.fromTextArea("tpl",  {
        parserfile: "parsexml.js",
        stylesheet: options.medi_path  +"/css/xmlcolors.css",
        path: options.medi_path + "/js/codemirror/",
        height: "450px"
      });      
      
      $("#templates").change(self.changeTemplate);
      $("#bempty").click(function(e) {
        e.preventDefault();
        $("#tpl_"+ self.current_template).val("");
        self.cde.setCode("");
        return false;
      });
       
      $("#templates").parents("form").submit(function() {
        $("#tpl_"+ self.current_template).val(self.cde.getCode());
      });
    }

    function init(options) {
      
      $.compono.storage.flush();
      
      var properties = {};
      
      // populate from old version
      if (options.doc) {
        var doc = options.doc;
        if ("_id" in doc) {
          self._id = doc['_id'];
          self._rev = doc['_rev'] || "";
          $("#name").val(doc.name);
        }
        
        // Initilize templates content
        if ("templates" in doc) {
          $("#tpl_show").val(doc.templates['show'] || "");
          $("#tpl_list").val(doc.templates['list'] || "");
        }
        
        if ("props" in doc) {
          // populate properties
          $.each(doc.props, function(idx, prop) {
            self.nb_fields += 1;
            self.add_widget(prop);
          })
        }
        
        if ("editors" in doc) {
          $("#editors").find("option").each(function() {
            if ($.inArray($(this).attr("value"), doc.editors)) {
              $(this).attr("selected", "selected")
            }
          });
        }
      }
         
      // some ui
      $("#tabs").tabs();
      $("input:submit").button();
       
      // init properties
      var property_path = self.property_path;
      $.each(options.properties, function(i, v) {
        $.getJSON(property_path + v + ".json", function(data) {
          self.available_properties[data.id] = data;
          $('<li><a href="#" id="' + data.id +'">'+data.label+'</a></li>')
          .click(self.add_type)
          .appendTo('#fieldsTypes');
        });
      });
      
      init_templates(options);
      $("#fedit").submit(self.saveType);
    }
    
    init(options);
  }
  
  $.compono = $.compono || {};
  $.extend($.compono, {
    createType: Type
  });
})(jQuery);