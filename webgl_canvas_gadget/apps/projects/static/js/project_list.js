;(function ( $, window, document, undefined ) {
	var pluginName = 'cgProjectList',
	defaults = {
		'card_list_view': '/billing/card/',
		'card_add_view': '/billing/card/add/',
		'card_change_active_view': '/billing/card/change_active/',
		'csrf_token': '',
	};
	
	function CGProjectList( element, options ) {
        this.element = element;
        this.$element = $(element);
        this.options = $.extend( {}, defaults, options) ;

        this._defaults = defaults;
        this._name = pluginName;
        
        this.init();
    }

	CGProjectList.prototype = {
		init: function () {
			var self = this;
			self.$modal = $('#modal');
			this.bindUI();
	    },
	    bindUI: function(){
	    	var self = this;
	    	
	    	self.$element.on('click', '.project-item[data-id] .link-project-detail', function(e){
	    		e.preventDefault();
	    		var project_id = $(this).closest('.project-item[data-id][data-payment]').attr('data-id');
	    		var tmpl = nunjucks.render('modal_project_detail.html', {'id': project_id});
	    		self.$modal.html(tmpl).modal('show');
	    	});
	    	
	    	self.$element.on('click', '.project-item[data-id] .btn-publish', function(e){
	    		e.preventDefault();
	    		var payment_url = $(this).closest('.project-item[data-id][data-payment]').attr('data-payment');
	    		var order_details = $(this).closest('.project-item[data-id]').attr('data-order-detail');
	    		self.selectCard(order_details, function(){
	    			self.publishProject(payment_url);
	    		})
	    	});
	    	
	    	self.$element.on('click', '.project-item[data-id] .btn-unpublish', function(e){
	    		e.preventDefault();
	    		$(this).button('loading');
	    		var payment_url = $(this).closest('.project-item[data-id][data-payment]').attr('data-payment');
	    		self.unpublishProject(payment_url);
	    	});
	    },
	    
	    selectCard: function(order_details, callback){
	    	var self = this;
	    	
	    	$.ajax({
				method: "GET",
				url: self.options['card_list_view'],
	    	}).success(function(data){
	    		if(data.card_list.length == 0 || data.default_card == null){
	    			//create new card if customer don't have card
	    			self.renderCardAddModal(order_details, callback);
	    		}else{
	    			//render select card form
	    			self.renderCardSelectModal(data, order_details, callback);
	    		}
	    	})
	    },
	    
	    publishProject: function(payment_url){
	    	var self = this;
	    	$.ajax({
				type:"GET",
				dataType: 'json',
				url: payment_url,
				data: {
					'action': 'publish'
				},
				success: function(data){
					var tmpl = $(nunjucks.render('project_item.html', {'project': data}));
					self.$element.find('[data-id][data-payment="' + payment_url + '"]').replaceWith(tmpl);
					self.$modal.modal('hide');
				},
				error: function(XMLHttpRequest, textStatus, errorThrown) {
					var tmpl = self.getErrorMessageHtml(XMLHttpRequest.responseJSON.error.message);
					self.$modal.find('.common-error').first().html(tmpl);
					
					self.$modal.find('.btn[type="submit"]').button('reset');
					self.$modal.find('fieldset').attr("disabled", false);
					console.log("subscription error", textStatus, errorThrown);
				},
			});
	    },
	    
	    unpublishProject: function(payment_url){
	    	var self = this;
	    	$.ajax({
				type:"GET",
				dataType: 'json',
				url: payment_url,
				data: {
					'action': 'unpublish'
				},
				success: function(data){
					var tmpl = $(nunjucks.render('project_item.html', {'project': data}));
					self.$element.find('[data-id][data-payment="' + payment_url + '"]').replaceWith(tmpl);
					self.$modal.modal('hide');
				},
				error: function(XMLHttpRequest, textStatus, errorThrown) {
					console.log("subscription error", textStatus, errorThrown);
				},
			});
	    },
	    
	    getErrorMessageHtml: function(message){
	    	return $(nunjucks.render('error_message.html', {'message': message}));
	    },
	    
	    renderCardSelectModal: function(card_data, order_details, callback){
	    	var self = this;
			var tmpl = $(nunjucks.render(
				'card_select_modal.html', 
				{
					'csrf_token': self.options['csrf_token'],
					'action': self.options['card_change_active_view'],
					'order_details': order_details,
					'card_list': card_data['card_list'],
					'default_card': card_data['default_card'], 
				}
			));
			
			tmpl.find('#btn-addcard').click(function(){
				self.renderCardAddModal(order_details, callback);
			});
			
			tmpl.find('#form-select-card').on('submit', function(e) {
				e.preventDefault();
				var form = $(this);
				
				$.ajax({
					type:"POST",
					dataType: 'json',
					url: form.attr('action'),
					data: form.serialize(),
					beforeSend: function(){
						form.find('.btn[type="submit"]').button('loading');
			    		form.closest('fieldset').attr("disabled", true);
					},
					success: function(data){
						if(callback){
							callback();
						}
					},
					error: function(XMLHttpRequest, textStatus, errorThrown) {
						console.log("can not change active card", textStatus, errorThrown);
					},
				});
			});
			
			self.$modal.html(tmpl).modal('show');
	    },
	    
	    renderCardAddModal: function(order_details, callback){
	    	var self = this;
			var tmpl = $(nunjucks.render(
				'card_add_modal.html', 
				{
					'action': self.options['card_add_view'],
					'csrf_token': self.options['csrf_token'],
					'order_details': order_details,
				}
			));
			
			tmpl.find('#form-add-card').on('submit', function(e) {
				e.preventDefault();
				
				var form = $(this);
				form.find('.btn[type="submit"]').button('loading');
				form.closest('fieldset').attr("disabled", true);
	    		
	    		function addFieldError(field_id, msg){
	        		form.find('.text-error').html('')
	        		$('#div_' + field_id + ' .text-error').html(msg);
	        	}
	    		
	    		var card = {
	                number: form.find('input[name="acct"]').first().val(),
	                cvc: form.find('input[name="cvv2"]').first().val(),
	                exp_month: form.find('select[name="expdate_0"]').first().val(),
	                exp_year: form.find('select[name="expdate_1"]').first().val()
	            };
	    		
		        Stripe.card.createToken(card, function(status, response){
		        	if(response.error){
	        			var tmpl = self.getErrorMessageHtml(response.error.message);
						self.$modal.find('.common-error').first().html(tmpl);
						
			            form.find('.btn[type="submit"]').button('reset');
			            form.closest('fieldset').attr("disabled", false);
			        }else{
			            var token = response.id;
			            form.find('input[name="stripe_token"]').first().val(token);
			            form.closest('fieldset').attr("disabled", false);
			            $.ajax({
							type:"POST",
							dataType: 'json',
							url: form.attr('action'),
							data: form.serialize(),
							beforeSend: function(){
								form.find('.btn[type="submit"]').button('loading');
					    		form.closest('fieldset').attr("disabled", true);
							},
							success: function(data){
								if(callback){
					    			callback();
					    		}
							},
							error: function(XMLHttpRequest, textStatus, errorThrown) {
								var tmpl = self.getErrorMessageHtml(XMLHttpRequest.responseJSON.error.message);
								self.$modal.find('.common-error').first().html(tmpl);
								
								console.log("some error", textStatus, errorThrown);
								form.find('.btn[type="submit"]').button('reset');
								form.closest('fieldset').attr("disabled", false);
							},
						});
			        }
		        });
			});
			self.$modal.html(tmpl).modal('show');
	    },
    }
	
	$.fn[pluginName] = function ( options ) {
		return this.each(function () {
			if (!$.data(this, 'plugin_' + pluginName)) {
			    $.data(this, 'plugin_' + pluginName,
			    new CGProjectList( this, options ));
			}
        });
    }
})( jQuery, window, document );