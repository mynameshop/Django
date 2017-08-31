function bindMentionsTextarea(element) {
    $(element).atWho('@', function (query, callback) {
        $.ajax({
            url: '/mentions',
            data: {'username': query},
            success: function (data) {
                callback(data);
            }
        });
    });
}

function dropDuplicateMentions(element) {
     $(element).find('a.mention-href').each(function () {
        if ($(this).text()=='@') {
            $(this).remove();
        }
     });
}

function mentionToHref(element) {
    var text = $(element).html();
    var pattern = /\B@[a-z0-9_-]+/gi;

    matches = text.match(pattern);
    href_template = '<a class="mention-href" href="[link]">[match]</a>';

    for (var i in matches) {
        match_un = matches[i].replace('@', '');
        href = href_template.replace('[link]', '/' + match_un).replace('[match]', match_un);
        text = text.replace(matches[i], href);
    }

    $(element).html(text);

    $(element).find('a.mention-href').each(function () {
        $(this).text('@' +$(this).text());
    });
    
    dropDuplicateMentions(element);

}

function mentionsTextReplace(text) {
    var pattern = /\B@[a-z0-9_-]+/gi;
    matches = text.match(pattern);
    href_template = '<a class="mention-href" href="[link]">[match]</a>';
    for (var i in matches) {
        match_un = matches[i].replace('@', '');
        href = href_template.replace('[link]', '/' + match_un).replace('[match]', match_un);
        text = text.replace(matches[i], href);
    }
    return text;
}

function markMentions(selector) {
    $(selector).each(function () {
        mentionToHref($(this));

    });
}

$(function () {
  

});