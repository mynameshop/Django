$(document).ready(function() {
	var elem = $("#socials.scroll_to");
	if(elem.length > 0) {
	    $('html, body').animate({
	        scrollTop: elem.offset().top
	    }, 400);
	}
});

var enableSubmitButton = function(){
	var btn = $('#submitBtn');
	btn.prop('disabled', false);
}

var disableSubmitButton = function(){
	var btn = $('#submitBtn');
	btn.prop('disabled', true);
}