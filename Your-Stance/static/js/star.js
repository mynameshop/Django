var StarHelper = function (selector) {
    var self = this;
    this.selector = selector;
    
    this.star = function (element) {
        $.ajax({
           url: $(element).attr('href'),
           dataType: 'json'
        }).success(function (data) {
            if(data.ok) {
                if(data.starred) {
                    $(element).text($(element).data('starred-text'));
                } else {
                    $(element).text($(element).data('notstarred-text'));
                }
                parent = $(element).parent();
                parent.find('.star-stance-counter').text(data.num_stars);
                var counter_label = parent.find('.star-counter-label');
                
                if(data.num_stars == 1) {
                    label = counter_label.data('single');
                } else {
                    label = counter_label.data('plural');
                }
                
                counter_label.text(label);
                
            } else {
                if (data.redir) {
                    window.location.href = data.redir;
                }
            }
        });
    };
    
    this.init = function () {
        $(document).on('click', self.selector, function (e) {
           e.preventDefault(); 
           self.star($(this));
        });
    };
    
    this.init();
};