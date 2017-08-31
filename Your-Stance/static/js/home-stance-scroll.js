var HomeFeedList = function (selector, offsetY, stanceTextFolder, htmlParser) {
    var self = this;

    this.selector = selector;
    this.scrolling = false;
    this.current_i = $(selector).data('per-page');
    this.per_page = $(selector).data('per-page');
    this.no_more_entries = false;
    this.offsetY = offsetY;
    this.stanceTextFolder = stanceTextFolder;
    this.htmlParser = htmlParser;

    this.loadNext = function (notAsync) {
        //console.log('loadNext');
        var async = true;
        if (notAsync) {
            async = false;
        }
        $('#stancelistLoading').show();
        self.scrolling = true;
        $.ajax({
            url: $(self.selector).data('url'),
            async: async,
            data: {
                from: self.current_i
            }
        }).success(function (data) {

            $('#stancelistLoading').hide();

            self.scrolling = false;

            data = mentionsTextReplace(data);
            $(self.selector).append(data);
            self.rebind();
            loaded_count = self.getLoadedCount();
            if (loaded_count == 0) {
                self.no_more_entries = true;
            }
            self.current_i += loaded_count;

        });
    };

    this.getLoadedCount = function () {
        count = $(self.selector).find('input.feed-loaded-count').last().val();
        if (count) {
            count = parseInt(count);
        } else {
            count = 0;
        }
        //console.log('getLoadedCount', count);
        return count;
    };

    this.scroll = function (e) {
        if (self.scrolling || self.no_more_entries) {
            return;
        }


        if ($(window).scrollTop() == $(document).height() - $(window).height()) {
            self.loadNext();
        }

    };

    this.getMovePos = function (skipOffsetY) {
        var pos = $(self.selector).position();
        movepos = $(document).height() - $(self.selector).height() - pos.top;
        if (skipOffsetY) {
            return movepos;
        } else {
            return movepos + self.offsetY;
        }

    };



    this.checkIfTooSmall = function () {
        var
                pos = $(self.selector).position(),
                wh = $(window).height(),
                movepos = $(self.selector).outerHeight(true) + pos.top,
                max_tries = 2,
                i = 0
                ;
        while (movepos < wh && i < max_tries) {
            movepos = $(self.selector).outerHeight(true) + pos.top;
            self.loadNext(true);
            i++;
        }
    };

    this.bind = function () {
        self.current_i = self.getLoadedCount();

        $(window).scroll(function () {
            self.scroll();
        });
    };

    this.rebind = function () {
        self.stanceTextFolder.initFor('.homeStanceContent');
        self.htmlParser.parseEach('.parsable');
        //mentionToHref(self.selector);
        //self.remarkMentions('.homeStanceContent');
    };

    if ($('body').find(self.selector).length === 0) {
        return;
    }

    this.bind();
    this.rebind();
    //this.checkIfTooSmall();

};


$(function () {

});