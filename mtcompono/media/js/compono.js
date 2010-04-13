/* This file is part of compono released under the Apache 2 license. 
 See the NOTICE for more information. */

String.prototype.startsWith = function(str) {
   return (this.match("^"+str)==str);
};


(function($) {
  
    var config = {
      toolbar:
      [
      ['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 
      'Unlink'], 
      ['UIColor']
      ]
    };
    
    
    function Storage() {
      
      this._storage = {};
      
      this._storage_service = {componoStorage:"{}"};
      
      this._storage_elm = null;

      this._init = function() {
        if ("localStorage" in window) {
          this._storage_service = window.localStorage;
        } else if ("globalStorage" in window) {
          this._storage_service = window.globalStorage[document.domain];
        } else {
          /* Check if browser supports userData behavior */
          this._storage_elm = document.createElement('link');
          if("addBehavior" in this._storage_elm){
            /* Use a DOM element to act as userData storage */
						this._storage_elm.style.behavior = 'url(#default#userData)';
						
						/* userData element needs to be inserted into the DOM! */
						document.getElementsByTagName('head')[0]
						        .appendChild(this._storage_elm);
						
						this._storage_elm.load("componoStorage");
						try{
							var data = this._storage_elm.getAttribute("componoStorage")
						}catch(E){var data = "{}"}
						if(data && data.length){
							this._storage_service.jStorage = data;
						}
					}else{
						this._storage_elm = null;
						return;
					}
        }
        /* if jStorage string is retrieved, then decode it */ 
				if ("componoStorage" in this._storage_service && this._storage_service.componoStorage) {
					try{
						this._storage = JSON.parse(this._storage_service.componoStorage);
					} catch(E){
					  this._storage_service.componoStorage = "{}";
					}
				}else{
					this._storage_service.componoStorage = "{}";
				}
      };
      
      this._save = function() {
        if(this._storage_service){
					try{
						this._storage_service.componoStorage = JSON.stringify(this._storage);
					}catch(E){/* probably cache is full, nothing is saved this way*/}
					// If userData is used as the storage engine, additional
					if (this._storage_elm) {
						try {
							this._storage_elm.setAttribute("componoStorage",
							                    this._storage_service.componoStorage)
							this._storage_elm.save("componoStorage");
						} catch(E){ }
					}
				}
      };
      
      this._checkKey = function(key) {
        if(!key || (typeof key != "string" && typeof key != "number")){
					throw new TypeError('Key name must be string or numeric');
				}
				return true;
      };
      
      ////////////////////////// PUBLIC METHODS /////////////////////////
			
			/**
			 * Sets a key's value.
			 * @param {String} key - Key to set. If this value is not set or not
			 * 						a string an exception is raised.
			 * @param value - Value to set. This can be any value that is JSON 
			 * 				 compatible (Numbers, Strings, Objects etc.).
			 * @returns the used value
			 */
			this.set = function(key, value){
				this._checkKey(key);
				this._storage[key] = value;
				this._save();
				return value;
			};
			
			/**
			 * Looks up a key in cache
			 * @param {String} key - Key to look up.
			 * @param {mixed} def - Default value to return, if key didn't exist.
			 * @returns the key value, default value or <null>
			 */
			this.get = function(key, def){
				this._checkKey(key);
				if(key in this._storage)
					return this._storage[key];
				return def?def:null;
			};
			
			/**
			 * Deletes a key from cache.
			 * @param {String} key - Key to delete.
			 * @returns true if key existed or false if it didn't
			 */
			this.deleteKey = function(key){
				this._checkKey(key);
				if(key in this._storage){
					delete this._storage[key];
					this._save();
					return true;
				}
				return false;
			};
			
			/**
			 * Deletes everything in cache.
			 * @returns true
			 */
			this.flush = function() {
				this._storage = {};
				this._save();
				return true;
			}
      
      this._init();
    }

    $.compono = $.compono || {};
    
    $.extend($.compono, {
      
        storage: new Storage(),
      
        editor: function(el) {
          $(el).ckeditor(config);
        },
        
        code_editor: function(el, options) {
          var element = el.element;
          
          self.cde = new CodeMirror.fromTextArea(el,  {
            parserfile: "parsexml.js",
            stylesheet: options.media_path  +"/css/xmlcolors.css",
            path: options.media_path + "/js/codemirror/",
            height: options.height
          });
          
        },
        
        load: function(path, callback) {
          var tpl = $.compono.storage.get(path);
          if (!tpl) {
            $.get(path, function(response) {
              $.compono.storage.set(path, response);
              return callback(response);
            });
          } else { 
            return callback(tpl);
          }
        },
        
        partial: function(path, data, callback) {
            /* get template and apply values */
            var path = path;
            var tpl = $.compono.storage.get(path);
            if (!tpl) {
              $.get(path, function(response) {
                  $.compono.storage.set(path, response);
                  var html = Mustache.to_html(response, data);
                  callback(html);
              });
            } else {
              var html = Mustache.to_html(tpl, data);
              callback(html);
            }
        },
        
        queryArgs: function(  ) {
            var args = new Object();
            var query = location.search.substring(1);     
              // Get query string
            var pairs = query.split(",");
             // Break at comma
            for(var i = 0; i < pairs.length; i++) {
                var pos = pairs[i].indexOf('=');
                  // Look for "name=value"
                if (pos == -1) continue;
                  // If not found, skip
                var argname = pairs[i].substring(0,pos);
                  // Extract the name
                var value = pairs[i].substring(pos+1);
                  // Extract the value
                args[argname] = unescape(value);
                 // Store as a property
               // In JavaScript 1.5, use decodeURIComponent(  ) 
               // instead of escape(  )
            }
            return args;     // Return the object
        }
        
        
    });
    
})(jQuery);