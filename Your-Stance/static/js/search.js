var SearchHelper = function () {
    var self = this;

    this.questionsBh = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: '/search_ajax/?type=questions&q=%QUERY',
            wildcard: '%QUERY'
        }
    });

    this.profileBh = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: '/search_ajax/?type=profiles&q=%QUERY',
            wildcard: '%QUERY'
        }
    });

    this.setupTypeAhead = function () {
        $('#topSearchBar input[name=search]').typeahead({
            highlight: true
        },
        {
            name: 'questions',
            source: self.questionsBh,
            display: 'slug',
            templates: {
                header: '<h3 class="searchHeader">Questions</h3>',
                suggestion: Handlebars.compile('<div data-slug="{{slug}}" class="questionSuggestion">{{slug}}</div>')
            }
        },
        {
            name: 'profiles',
            source: self.profileBh,
            display: 'user__username',
            templates: {
                header: '<h3 class="searchHeader paddedHeader">Profiles</h3>',
                suggestion: Handlebars.compile('<div data-slug="{{user__username}}" class="profileSuggestion">{{user__username}}</div>')
            }
        }
        );
    };

    this.bind = function () {
        
        $(document).on('click', '.profileSuggestion', function () {
            window.location.href = '/' + $(this).data('slug');
        });
        
        $(document).on('click', '.questionSuggestion', function () {
            window.location.href = '/q/' + $(this).data('slug');
        });
        
        $('#topSearchBar').on('keyup', 'input[name=search]', function(e) {
            if(e.keyCode === 13) {
               $('.tt-menu').find(".tt-suggestion").first().click();
           }
        });
        
    };

    this.setupTypeAhead();
    this.bind();
};


$(function () {
    new SearchHelper();
});

