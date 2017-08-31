var followRequest = function (element) {
//     window.location.href = $(element).data('href');
//     return;
    $.ajax({
        url: $(element).data('href'),
        method: 'POST',
        dataType: 'json',
        success: function (data) {
            
            if (data.ok) {
                if (data.followed) {
                    $(element).text($(element).data('unfollow-label'));
                    $(element).attr('data-followed', '1');
                } else {
                    $(element).text($(element).data('follow-label'));
                    $(element).attr('data-followed', '0');
                }
            }
            
        }
    });
};

$(function () {
    $('.followBtn').click(function (e) {

        e.preventDefault();
        followRequest(this);

    });
});