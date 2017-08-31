;(function ( $, window, document, undefined ) {
	var pluginName = 'panelTabbedCollapse',
	defaults = {};
	
	function PanelTC( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options);
        this._defaults = defaults;
        this._name = pluginName;
        
        this.init();
    }

	PanelTC.prototype = {
		init: function () {
			this.initElements();
			this.bindUI();
	    },
	    initElements: function(){
	    	this.$element = $(this.element);
	        this.$panel_body = this.$element.find('.panel-body').first();
			this.$panel_header = this.$element.find('.panel-heading').first();
			this.$tabs = this.$element.find('a[href][role="tab"]');
	    },
	    bindUI: function(){
	    	var self = this;
	    	
	    	self.onresize();
	    	$(window).resize(function() {
	    		self.onresize();
			});
	    	
	    	self.$tabs.click(function(e){
	    		var $tab = $(this);
	    		self.changeActive($tab);
	    		e.preventDefault();
	    	});
	    	
	    	self.$panel_body.on('hidden.bs.collapse', function () {
	    		self.$panel_body.children('.tab-content').addClass('hidden');
	    	})
	    },
	    
	    onresize: function(){
	    	this.$panel_body.css('max-height', $(window).height()-38-45+'px');
	    },
	    
	    changeActive: function($tab){
	    	var self = this;
	    	self.$tabs.each(function(i, item){
	    		if($(item).attr('href') !== $tab.attr('href')){
	    			$(item).parent().removeClass('active');
	    			self.$panel_body.find($(item).attr('href')).addClass('hidden')
	    		}else{
	    			if($tab.parent().toggleClass('active').hasClass('active')){
	    				self.$panel_body.find($tab.attr('href')).removeClass('hidden')
	    				self.$panel_body.collapse('show');
	    			}else{
	    				self.$panel_body.collapse('hide');
	    			}
	    		}
	    	});
	    },
    }
	
	$.fn[pluginName] = function ( options ) {
		return this.each(function () {
			if (!$.data(this, 'plugin_' + pluginName)) {
			    $.data(this, 'plugin_' + pluginName,
			    new PanelTC( this, options ));
			}
        });
    }
})( jQuery, window, document );