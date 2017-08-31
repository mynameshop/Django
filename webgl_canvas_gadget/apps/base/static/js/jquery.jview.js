;(function ( $, window, document, undefined ) {
	var pluginName = 'jView',
	defaults = {
		delegate : function(i, data){return ''},
		refreshed : function(self){},
	};
	
	function JView( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options );

        this._defaults = defaults;
        this._name = pluginName;
        
        this.init();
    }

	JView.prototype = {
		init: function () {
			this.initElements();
			this.bindUI();
			this.refresh();
	    },
	    initElements: function(){
	    	this.$element = $(this.element);
	    	this.$model = $(this.$element.attr('jmodel'));
	    	this.$target = this.$element.attr('jtarget') ? $(this.$element.attr('jtarget')) : this.$element;
	    },
	    bindUI: function(){
	    	var self = this;
	    	self.$model.change(function(){
	    		self.refresh();
	    	})
	    },
	    refresh: function(){
	    	var data = this.$model.val() ? $.parseJSON(this.$model.val()) : [];
	    	var template = '';
	    	for(var i = 0; i < data.length; i++){
    			template += this.options.delegate(i, data[i]);
    		}
	    	this.$target.html(template);
	    	this.options.refreshed(this);
	    },
    }
	
	$.fn[pluginName] = function ( options ) {
		return this.each(function () {
			if (!$.data(this, 'plugin_' + pluginName)) {
			    $.data(this, 'plugin_' + pluginName,
			    new JView( this, options ));
			}
        });
    }
})( jQuery, window, document );