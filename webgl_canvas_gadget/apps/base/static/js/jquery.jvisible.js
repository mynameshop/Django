;(function ( $, window, document, undefined ) {
	var pluginName = 'jVisible',
	defaults = {
		checkState: function($model){
			return $model.is(':checked');
		}
	};
	
	function JVisible( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options );

        this._defaults = defaults;
        this._name = pluginName;
        
        this.init();
    }

	JVisible.prototype = {
		init: function () {
			this.initElements();
			this.bindUI();
			this.refresh();
	    },
	    initElements: function(){
	    	this.$element = $(this.element);
	    	this.$model = $(this.$element.attr('jmodel'))
	    },
	    bindUI: function(){
	    	var self = this;
	    	self.$model.change(function(){
	    		self.refresh();
	    	})
	    },
	    refresh: function(){
	    	var prop = {};
	    	var animate = 'hide';
	    	if(this.options.checkState(this.$model)){
	    		animate = 'show';
	    	}
	    	$.each(this.$element.attr('janimation').replace(/ /g,'').split(','), function(i, data){
	    		prop[data] = animate;
	    	});
	    	this.$element.animate(prop, 400, function() {});
	    },
    }
	
	$.fn[pluginName] = function ( options ) {
		return this.each(function () {
			if (!$.data(this, 'plugin_' + pluginName)) {
			    $.data(this, 'plugin_' + pluginName,
			    new JVisible( this, options ));
			}
        });
    }
})( jQuery, window, document );