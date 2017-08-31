var FriendList = function () {
    var self = this;
    this.container = $('#firendlistContainer');
    this.currentType = null;
    this.fbimgLimit = 10;
    this.loadFBImages = function () {
        $(this.container).find('input[name=extra-data]').each(function () {
            extraData = $.parseJSON($(this).val());
            var photosContainer = $(this).parent();
            if (extraData.fbid) {
                access_token = extraData.token;
                url = 'https://graph.facebook.com/' + extraData.fbid + '/albums?access_token=' + access_token;

                FB.api(url, 'GET', {}, function (result) {

                    if (result.data) {
                        profile_album = null;

                        for (var i in result.data) {
                            if (result.data[i].type == 'wall') {
                                profile_album = result.data[i].id;
                                break;
                            }
                        }

                        if (profile_album) {
                            url = 'https://graph.facebook.com/' + profile_album + '/photos?access_token=' + access_token;
                            FB.api(url, 'get', function (result) {
                                if (result.data && result.data.length) {
                                    for (var i in result.data) {
                                        if (i >= self.fbimgLimit) {
                                            break;
                                        }
                                        $(photosContainer).append('<img src=' + result.data[i].source + ' />');
                                    }
                                }
                            });
                        }
                    }

                });

            }
        });
    };

    this.loadGoogleImages = function () {
        $(self.container).children().find('table tbody tr').each(function () {
            extra_data = $.parseJSON($(this).find('input[name=extra-data]').val());
            img = $(this).children().find('img');

            $(img).attr('src', extra_data.google_avatar);
            console.log('extra_data', extra_data);
        });
    };

    this.afterLoad = function (data) {
        if (self.currentType == 'fb') {
            self.loadFBImages();
        } else if (self.currentType == 'gmail') {
            //self.loadGoogleImages();
        } else {

        }
    };

    this.fetchFriends = function (type, init) {

        self.currentType = type;
        self.loading(true);
        if (init) {
            self.resetPaging();
            $(self.container).html('');
        }
        $('#moreFriends').parent().hide();
        $.ajax({
            url: $(self.container).data('url'),
            data: {
                'type': type,
                'max_res': self.max_res,
                'next': $(self.container).children().find('table').data('next'),
            }
        }).success(function (data) {
            hideMore = $(data).find('input[name=hideMore]').val();

            if (hideMore == 0) {
                $('#moreFriends').parent().show();
            }

            if (init) {
                $(self.container).html(data);
                self.loading(false);
                self.afterLoad(data);
            } else {

                next = $(data).find('table').data('next')
                if (next == 'None') {
                    self.no_more = true;
                }
                $(self.container).find('table tbody').append($(data).children().find('tbody').html());
                $(self.container).find('table').data('next', next);

                self.loading(false);
                self.afterLoad(data);
            }

        });
    };

    this.bindSelect = function () {
        $('#firendlistServiceSelect a').click(function (e) {
            e.preventDefault();

            self.fetchFriends($(this).attr('href'), true);
            $('#firendlistServiceSelect a').removeClass('active');
            $(this).addClass('active');
        });

        var service = $('#firendlistServiceSelect').data('service');

        $('#firendlistServiceSelect a[href=' + service + ']').click();

    };

    this.fbInvite = function (element) {
        var to_uid = $(element).data('uid');
        FB.ui({method: 'apprequests',
            message: 'www.yourstance.com',
            link: 'http://www.yourstance.com',
            to: to_uid
        }, function (response) {
            console.log(response);
        });
    };

    this.gmailInvite = function (email) {
        var url = $(self.container).children().find('table').data('invite-url');
        console.log('invite', url);
        $.ajax({
            url: url,
            method: 'post',
            dataType: 'json',
            cache: false,
            data: {
                email: email
            }
        }).success(function (data) {
            console.log('invitation response', data);
        });
    };
    
    this.twitterInvite = function (uid) {
        console.log('inviting uid', uid);
        $.ajax({
           url: $(self.container).children().find('table').data('twitter-invite-url'),
           method: 'post',
           dataType: 'json',
           cache: false,
           data: {
               uid: uid
           }
        }).success(function (data) {
            console.log('twitter invite response', data);
        });
    }
    
    this.bindInvite = function () {
        $(self.container).on('click', '.invite-button', function (e) {
            if ($(this).data('type') == 'fb') {
                self.fbInvite($(this));
            } else if (self.currentType == 'gmail') {
                //self.gmailInvite($(this));
                email = $.parseJSON($(this).parent().parent().find('input[name=extra-data]').val());
                self.gmailInvite(email);
            } else if (self.currentType == 'twitter') {
                self.twitterInvite($(this).data('uid'));
            }

        });
    };

    this.bindFollow = function () {
        $(self.container).on('click', '.friendFollowBtn', function (e) {

            e.preventDefault();
            followRequest(this);

        });

        $(self.container).on('click', '.friendListFollowAll', function (e) {
            e.preventDefault();
            console.log('follow all clicked');
            $(self.container).find('.friendFollowBtn').each(function () {
                if ($(this).attr('data-followed') != '1') {
                    $(this).click();
                }
            });
        });
    };

    this.resetPaging = function () {
        $(self.container).children().find('table').data('next', '');
        self.max_res = 10;
        self.no_more = false;
    };

    this.bindMore = function () {
        $('#moreFriends').click(function (e) {
            if (!self.no_more) {
                self.fetchFriends(self.currentType, false);
            }
        });
    };

    this.loading = function (isLoading) {
        if (isLoading) {
            $('.friendListSpinner').show();
        } else {
            $('.friendListSpinner').hide();
        }
    };


    this.resetPaging();
    this.bindSelect();
    this.bindInvite();
    this.bindFollow();
    this.bindMore();
};