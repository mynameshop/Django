/*
 * TODO:
 * fix linebreaks problem
 */
var ParseHTML = function (selector) {
    var self = this;
    this.selector = selector;
    
    this.getVId = function (url) {
        if (!url) {
            return '';
        }

        var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
        var match = url.match(regExp);
        var image_url = '';

        if (match && match[7].length == 11) {
            return match[7];
        }
    };
    
    this.dropBr = function(text) {
        var bri = text.indexOf('<br>');
        if(bri!==-1) {
            text = text.substring(0, bri);
        }
        return text; 
    };
    
    this.parse = function (element, force) {
        
        if($(element).data('parsed') && !force) {
            return;
        }
        
        var 
            urlRegex = new RegExp(/(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/g),            
            hrefTemplate = '<a href="[[url]]" target="_blank">[[label]]</a>',
            videoTemplate = '<iframe class="ytIframe" type="text/html" '+
                'src="https://www.youtube.com/embed/[[vid]]" '+
                'frameborder="0"></iframe>';
        ;
        
        $(element).data('parsed', '1');
        text = $(element).html();
        
        urls = text.match(urlRegex);
        
        for(var i in urls) {
            vid = null;
            var url = self.dropBr(urls[i]);    
            
            if($(element).data('parse-urlonly')!='1') {
                vid = self.getVId(url);
            }
            
            if(vid) {
               video = videoTemplate.replace('[[vid]]',vid);
               text = text.replace(url, video);
            } else {
                href = hrefTemplate.replace('[[url]]', url).replace('[[label]]', url);
                text = text.replace(url, href);
            }
            
        }
        
        $(element).html(text);
        
    };
    
    this.parseEach = function (selector) {
      $(selector).each(function () {
          self.parse($(this));
      });
    };
    
    this.parseEach(this.selector);
    
};