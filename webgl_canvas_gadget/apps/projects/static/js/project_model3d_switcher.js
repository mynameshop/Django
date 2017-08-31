;(function ( $, window, document, undefined ) {
	var pluginName = 'projectModel3dSwitcher',
	defaults = {};
	
	function projectModel3dSwitcher( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options);

        this._defaults = defaults;
        this._name = pluginName;
        
        this.init();
    }

	projectModel3dSwitcher.prototype = {
		init: function () {
			this.initElements();
			this.bindUI();
			this.refresh();
	    },
	    renderItem: function(data){
	    	return $('<li data-id="'+data.pk+'">\
	    			<a href="#">\
						<img src="'+data.thumbnail+'" alt="img" style="width: 28px; height: 28px;">\
					</a>\
				</li>\
	    	');
	    },
	    initElements: function(){
	    	this.$element = $(this.element);
	    	this.$model = $(this.$element.attr('jmodel')).first();
	    	this.active = '';
	    },
	    bindUI: function(){
	    	var self = this;
	    	
	    	self.$model.on('change', function(){
	    		self.refresh();
	    	})
	    	
	    	self.$element.on('click', 'li[data-id] > a', function(e){
	    		var obj = $(this).parent();
	    		if(self.active !== obj.attr('data-id')){
		    		$("body").trigger({
	    				type: "modelChanged",
	    				tab: "models",
	    				model: obj.data('model'),
	    				textures: obj.data('textures'),
	    			});
	    		}
	    		e.preventDefault();
	    	})
	    },
	    refresh: function(){
	    	var self = this;
	    	var is_empty = (self.$element.children().size()===0);
	    	
	    	self.$element.empty();
	    	$.each($.parseJSON(self.$model.val().replace(/'/g, "\"")), function(i, data){
	    		var item = self.renderItem(data);
	    		item.data('model', data.file);
	    		item.data('textures', data.textures);
	    		self.$element.append(item);
	    	})
	    	if(is_empty){
	    		self.$element.children().first().children('a').click();
	    	}
	    },
    }
	
	$.fn[pluginName] = function ( options ) {
		return this.each(function () {
			if (!$.data(this, 'plugin_' + pluginName)) {
			    $.data(this, 'plugin_' + pluginName,
			    new projectModel3dSwitcher( this, options ));
			}
        });
    }
})( jQuery, window, document );