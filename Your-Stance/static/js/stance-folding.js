var TextFolder = function (selector, wordLimit) {
    var self = this;
    this.selector = selector;
    this.wordLimit = wordLimit;
    this.unfoldHtml = null;

    this.appendUnfoldToggle = function (element) {

        if (!self.unfoldHtml) {
            uh = document.createElement('span');
            $(uh).text(' ...');
            $(uh).addClass('unfoldToggle');
            self.unfoldHtml = uh;
        }

        $(element).append(self.unfoldHtml);

    };

    this.toggleShorten = function (element) {
        var
                ft = $(element).attr('data-full-text'),
                st = $(element).attr('data-short-text')
                ;



        if ($(element).attr('data-short') === '1') {
            $(element).attr('data-short', '0');
            $(element).html(ft);
        } else {
            $(element).attr('data-short', '1');
            $(element).html(st);
        }

        self.remarkMentions(element);

        self.appendUnfoldToggle(element);

    };

    this.remarkMentions = function (element) {
        if ($(element).hasClass('with-mentions')) {
            markMentions($(element));
        }
    };

    this.bindOnfoldToggles = function () {
        $(document).on('click', '.unfoldToggle', function (e) {
            e.stopImmediatePropagation();
            p = $(this).parent();
            self.toggleShorten(p);

        });
    };

    this.makeShorten = function (element) {

        var wl = self.wordLimit;

        if ($(element).attr('data-word-limit')) {
            wl = parseInt($(element).attr('data-word-limit'));
        }

        $(element).attr('data-short', '1');
        short_text = $(element).attr('data-short-text');
        if (!short_text) {

            words = $(element).html().split(' ');



            new_words = [];

            //First remove empty strings;
            for (var i = 0; i < words.length; i++) {
                if (words[i] !== '') {
                    new_words.push(words[i]);
                }
            }

            words = new_words;

            if (words.length <= wl) {
                return; //No need to shorten
            }

            short_text = '';

            for (var i = 0; i < Math.min(words.length, wl + 1); i++) {
                short_text = short_text + ' ' + words[i];
            }


            $(element).attr('data-full-text', $(element).html());
            $(element).attr('data-short-text', short_text);
            $(element).html((element).attr('data-short-text'));
            
            self.appendUnfoldToggle(element);
        }
    };

    this.initFor = function (selector) {

        $(selector).each(function () {
            self.makeShorten($(this));
            self.remarkMentions($(this));

        });

    };

    this.init = function () {
//        $('.foldable').each(function () {
//            self.makeShorten($(this));
//            self.remarkMentions($(this));
//
//        });
        this.initFor('.foldable');

        // this.bindOnfoldToggles();
    };

    this.init();
    this.bindOnfoldToggles();
};