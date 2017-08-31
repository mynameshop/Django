;(function ( $, window, document, undefined ) {
	var pluginName = 'projectEditor',
	defaults = {};
	
	function projectEditor( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options) ;

        this._defaults = defaults;
        this._name = pluginName;
        
        this.init();
    }

	projectEditor.prototype = {
		init: function () {
			this.initElements();
			this.bindUI();
	    },
	    initElements: function(){
	    	this.$element = $(this.element);
	    	this.checkboxes = this.$element.find('.editor-control[type="checkbox"][name]');
	    	this.ranges = this.$element.find('.editor-control[type="range"][name]');
	    	this.selects = this.$element.find('select[name]');
	    },
	    bindUI: function(){
	    	var self = this;
	    	
	    	self.checkboxes.change(function(){
	    		self.triggerChangeEvent($(this).attr('name'), $(this).is(':checked'));
	    	});
	    	
	    	self.ranges.on('input change', function(){
	    		self.triggerChangeEvent($(this).attr('name'), $(this).val());
	    	});
	    	
	    	self.selects.on('change', function(e){
	    		self.triggerChangeEvent($(this).attr('name'), $(this).children('option:selected').data('model'));
	    	});
	    },
	    get_json: function(){
	    	var data = {};
	    	$.each(this.checkboxes, function(i, item){
	    		data[$(item).attr('name')] = $(item).is(':checked');
	    	})
	    	$.each(this.ranges, function(i, item){
	    		data[$(item).attr('name')] = $(item).val();
	    	})
	    	$.each(this.selects, function(i, item){
	    		data[$(item).attr('name')] = $(item).val();
	    	})
	    	return data;
	    },
	    triggerChangeEvent: function(name, value){
			$("body").trigger({
				type: "editorPropertyChanged",
				tab: "environment",
				name: name,
				value: value,
			});
	    },
    }
	
	$.fn[pluginName] = function ( options ) {
		return this.each(function () {
			if (!$.data(this, 'plugin_' + pluginName)) {
			    $.data(this, 'plugin_' + pluginName,
			    new projectEditor( this, options ));
			}
        });
    }
})( jQuery, window, document );