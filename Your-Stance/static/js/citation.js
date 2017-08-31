var CitationHelper = function () {
    var self = this;


    this.isLink = function (citation) {
        citation = citation.trim();
        if(citation.startsWith('http://') || citation.startsWith('https://')) {
            return true;
        } else {
            return false;
        }
    };

    this.init = function () {
        $('.citationLinkContainer li').click(function (e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            window.location.href = $(this).data('href');
        });

        $('.citationLinkContainer a.citationLink').click(function (e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            
            if($(this).parent().data('has-dropdown')!='1') {
                window.location.href = $(this).attr('href');
            }
            
        });

        $('.citationLinkContainer').click(function (e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            
        });

        $('.citationLinkContainer').each(function () {
           var a = $(this).find('a.citationLink');
           if (self.isLink($(a).data('citation'))) {
                $(this).children().find('li.pageCitation').attr('data-href', $(a).attr('href'));
                $(this).children().find('li.linkCitation').attr('data-href', $(a).data('citation'));
                $(this).data('has-dropdown', '1');
            } else {
                $(this).data('has-dropdown', '0');
                $(this).find('.citationDropdown').remove();
            }
        });
    };

    this.init();
};
