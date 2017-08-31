$(function () {
    mention_selectors = [
        '#id_comment_text',
        '#id_stance_text',
        '.stance-form .stance-text'
    ];

    for (var i in mention_selectors) {

        bindMentionsTextarea($(mention_selectors[i]));
    }

    markMentions('.with-mentions');

    var htmlParser = new ParseHTML('.parsable');
    var stanceTextFolder = new TextFolder('.foldable', 100);
    var stanceHelper = new StanceAnswerHelper(htmlParser);

    new HomeFeedList('#home-stance-list', 0, stanceTextFolder, htmlParser);
    
    new ComparisonGrid('.comparisonSheet');
    new StarHelper('.star-stance-trigger');
    new CitationHelper();

});