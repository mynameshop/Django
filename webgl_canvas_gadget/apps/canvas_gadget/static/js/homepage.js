$(document).ready(function(){
	$(document).on('click', '.link-popup-iframe', function(e){
		e.preventDefault();
		$('#modal-iframe .canvasgadget-iframe').attr('src', $(this).attr('href')).focus();
		$('#modal-iframe').modal('show');
		_gaq.push(['_trackEvent', 'play_button', 'clicked', $(this).attr('href')]);
	})
	
	$('#modal-iframe').on('hidden.bs.modal', function (e) {
		$('#modal-iframe .canvasgadget-iframe').attr('src', '');
	})
	
	$('#modal-signin').on('shown.bs.modal', function (e) {
		$('#modal-signin').find('input[name="name"]').focus();
	})
	
	$('#contact-form').on('submit', function(e){
		var form = $(this);
		$.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            data: form.serialize(),
            success: function( data ) {
            	$('#contact-form')[0].reset()
    			$('#contact-form').closest('.modal').modal('hide');
            	window.location.href = '/pricing/'
            },
            error: function (xhr, status) {
                alert(status);
            },
        });
		e.preventDefault();
		return false;
	})
})