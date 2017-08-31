;(function ( $, window, document, undefined ) {
	var pluginName = 'jSelect',
	defaults = {
		delegate: function($option){
			return '';
		},
		refreshed: function(self){}
	};
	
	function Select( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options) ;

        this._defaults = defaults;
        this._name = pluginName;
        
        this.init();
    }

	Select.prototype = {
		init: function () {
			this.initElements();
			this.bindUI();
			this.repaint();
	    },
	    initElements: function(){
	    	this.$element = $(this.element);
	    	this.$model = $(this.$element.attr('jmodel'));
	    },
	    bindUI: function(){
	    	var self = this;
	    	self.$model.change(function(){
	    		self.$element.find('[data-value]').removeClass('active');
	    		self.$element.find('[data-value="' + self.$model.val() + '"]').addClass('active');
	    	})
	    	
	    	self.$model.on('optionChanged', function(){
	    		self.repaint();
	    	})
	    	
	    	self.$element.on('click mousedown', '[data-value]', function(e){
				e.preventDefault();
				if(!self.$model.find('option[value="' + $(this).data('value') + '"]').is(':selected') ){
					self.$model.val($(this).data('value')).change();
				}
			})
	    },
	    repaint: function(){
	    	var self = this;
	    	var html = '';
	    	self.$model.children().each(function(i, item){
	    		html += self.options.delegate($(item));
	    	})
	    	self.$element.html(html);
	    	self.refreshActive();
	    	self.options.refreshed(self);
	    },
	    refreshActive: function(){
	    	var self = this;
			self.$model.change();
		},
    }
	
	$.fn[pluginName] = function ( options ) {
		return this.each(function () {
			if (!$.data(this, 'plugin_' + pluginName)) {
			    $.data(this, 'plugin_' + pluginName,
			    new Select( this, options ));
			}
        });
    }
})( jQuery, window, document );