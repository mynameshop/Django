;(function ( $, window, document, undefined ) {
	var pluginName = 'uploader',
	defaults = {
		onSuccess : function(data){},
	};
	
	function Uploader( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options );

        this._defaults = defaults;
        this._name = pluginName;
        
        this.init();
    }

	Uploader.prototype = {
		init: function () {
			this.initElements();
			this.bindUI();
	    },
	    initElements: function(){
	    	this.$element = $(this.element);
	    },
	    bindUI: function(){
	    	var self = this;
	    	self.$element.on('submit', function(e){
				var form = $(this);
				var formData = new FormData(form[0]);
				form[0].reset();
				$.ajax({
		            url: form.attr('action'),
		            type: form.attr('method'),
		            processData: false,
		            contentType: false,
		            dataType: 'json',
		            data: formData,
		            success: function( data ) {
		            	self.options.onSuccess(data);
		            },
		        });
				e.preventDefault();
				return false;
	    	})
	    },
    }
	
	$.fn[pluginName] = function ( options ) {
		return this.each(function () {
			if (!$.data(this, 'plugin_' + pluginName)) {
			    $.data(this, 'plugin_' + pluginName,
			    new Uploader( this, options ));
			}
        });
    }
})( jQuery, window, document );