AjaxSpinner = {
    htmlTemplate: '<div class="[className]"><img src="[imgSrc]" /></div>',
    makeHtml: function (imgSrc, className) {
        if (!imgSrc) {
            imgSrc = '/static/images/ajax-loader-big.gif';
        }

        if (!className) {
            className = 'ajaxSpinnerContainer';
        }

        spinnerHtml = AjaxSpinner.htmlTemplate
                .replace('[className]', className)
                .replace('[imgSrc]', imgSrc);

        return spinnerHtml;

    }
};