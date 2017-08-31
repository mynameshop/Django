$(function() {
	window.scrollReveal = new scrollReveal();
	"use strict";
	
	// PreLoader
	$(window).load(function() {
		$(".loader").fadeOut(400);
	});

	// Backstretchs
	$("#header").backstretch("/static/images/3.jpg");
	$("#services").backstretch("/static/images/3.jpg");
	
	// Countdown
	$('.countdown').downCount({
		date: '12/12/2014 12:00:00',
		offset: +10
	});			
    
	// contact-form
	$('#contact-form').jAjaxForm({
		'onSuccess': function(data){
			$('#contact-form').reset();
		}
	})
	
});