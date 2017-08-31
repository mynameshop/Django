$(document).ready(function(){
	$('#jselect-pricing-template').jSelect({
		'delegate': function($option){
			var model = $option.data('model');
			var html = '<li>';
			html += '<a href="#" data-value="' + $option.val() + '" class="select-item">';
			html += '<div class="subscription_cost">$' + $option.text() + '</div>';
			html += '</a>';
			html += '</li>';
			return html;
		},
	});
	
	$('#select-pricing-template').on('change', function(){
		var $option = $(this).find('option[value="' + $(this).val() + '"]').first();
		$('#active-subscription-template a[data-id]').first().attr('data-id', $(this).val());
		$('#form-submit-project input[name="subscription_template"]').first().val($(this).val());
		$('#active-subscription-template .subscription_cost').first().html($option.text());
		$('#modal-select-pricing-template').modal('hide');
	}).change();
	
	$('#modal-select-pricing-template').on('shown.bs.modal', function(){
		$(document).resize();
	})
	
	$('#active-subscription-template a[data-id]').click(function(e){
		$('#modal-select-pricing-template').modal();
		e.preventDefault();
	})
	
	$("<div><b style='margin-right: 16px;' class='text-gray'>Upload photos or drawings of your product.</b><a href='#' class='btn-upload'>Upload Images<span class='glyphicon glyphicon-save'></span></a><div class='file-counter'></div></div>").insertAfter($('#form-submit-project input[name="images"]').first());
	
	$('#form-submit-project input[name="images"]').change(function(){
		var html = '';
		if($(this)[0].files.length > 0){
			html += $(this)[0].files.length + ' images have been uploaded <a href="#" class="remove-files">Remove Images</a>';
		}
		$('#form-submit-project .file-counter').html(html);
	})
	
	$(document).on('click', '.btn-upload', function(e){
		e.preventDefault();
		$('#form-submit-project input[name="images"]').first().click();
	})
	
	$(document).on('click', '.remove-files', function(e){
		e.preventDefault();
		$('#form-submit-project input[name="images"]').first().val('').change();
	})
	
	if($('#form-submit-project .error').length > 0){
		
		$('html, body').animate({
	        scrollTop: $('#form-submit-project').parent().offset().top
	    }, 600);
	}
})