/* This file is part of compono released under the Apache 2 license. 
 See the NOTICE for more information. */



(function($) {

    $.goldorak = $.goldorak || {};
    
    $.extend($.goldorak, {
        partial: function(path, data, callback) {
            /* get template and apply values */
            $.get(path, function(response) {
                var html = Mustache.to_html(response, data);
                callback(html);
            })
        },
        
    });
    
})(jQuery);