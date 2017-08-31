;(function ( $, window, document, undefined ) {
	var pluginName = 'inactivityTime',
	defaults = {
		timeout: 10000,
		inactivityCallback: function(){
			console.log('inactivity');
		},
		activityCallback: function(){
			console.log('activity');
		},
	};
	
	function InactivityTime( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options) ;

        this._defaults = defaults;
        this._name = pluginName;
        
        this.init();
    }

	InactivityTime.prototype = {
		init: function () {
			this.initElements();
			this.bindUI();
	    },
	    initElements: function(){
	    	this.$element = $(this.element);
	    	this.timer = 0;
	    	this.state = '';
	    },
	    bindUI: function(){
	    	var self = this;
	    	self.$element.on('mousemove keypress touchstart mousedown click', function(e){
	    		self._resetTimer();
	    	});
	    	self._resetTimer();
	    },
	    _resetTimer: function(){
	    	clearTimeout(this.timer);
	    	this.timer = setTimeout(this._inactivity.bind(this), this.options.timeout);
	    	this._activity();
	    },
	    _inactivity: function(){
	    	if(this.state === 'inactive'){
    			return;
    		}
	    	this.state = 'inactive';
	    	this.options.inactivityCallback();
	    },
	    _activity: function(){
	    	if(this.state === 'active'){
    			return;
    		}
	    	this.state = 'active';
	    	this.options.activityCallback();
	    },
    }
	
	$.fn[pluginName] = function ( options ) {
		return this.each(function () {
			if (!$.data(this, 'plugin_' + pluginName)) {
			    $.data(this, 'plugin_' + pluginName,
			    new InactivityTime( this, options ));
			}
        });
    }
})( jQuery, window, document );