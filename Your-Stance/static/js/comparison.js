var ComparisonGrid = function (containerSelector) {
    var self = this;
    this.containerSelector = containerSelector;
    this.more = false;
    this.lock = false;

    this.fetch = function (refetch) {
        self.lock = true;
        if (refetch) {

            $(self.containerSelector).find('input[name=type]').val('refetch');
        } else {
            $(self.containerSelector).find('input[name=type]').val('comparision');
        }
        var data = $(self.containerSelector).find('input.sheet_field').serialize();


        $.ajax({
            url: $(self.containerSelector).data('url'),
            method: 'get',
            data: data,
        }).success(function (data) {
            if ($(self.containerSelector).find('input[name=type]').val() == 'refetch') {
                $(self.containerSelector).html(data);
                self.bindSelect2();
                $(self.containerSelector).find('input[name=type]').val('comparision');
            } else {
                $(self.containerSelector).find('.sheet-items').append(data);
            }
            self.lock = false;

        });
    };

    this.bindSelect2 = function () {
        function formatRepo(repo) {
            if (repo.loading)
                return repo.text;

            var markup = repo.username;

            return markup;
        }
        function formatRepoSelection(repo) {
            return repo.username;
        }
        $(self.containerSelector).children().find('.comparableSelect').select2({
            ajax: {
                url: "/users_ajax",
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        username: params.term, // search term

                    };
                },
                processResults: function (data, params) {

                    return {
                        results: data,
                    };
                },
                cache: true
            },
            escapeMarkup: function (markup) {
                return markup;
            },
            templateResult: formatRepo,
            templateSelection: formatRepoSelection,
            width: '100%'
        }).on('select2:select', function (e) {
            $(self.containerSelector).find('.sheet-users').append(
                    '<input type="hidden" name="user_pk[]" class="sheet_field" value="'
                    + e.params.data.id +
                    '" />'
                    );

            self.toggleComparableSelect();
            self.fetch(true);
        });
    };

    this.toggleComparableSelect = function () {
        $(self.containerSelector).children().find('.comparableContainer').toggle();
    };

    this.init = function () {

        this.limit_step = parseInt($(self.containerSelector).find('input[name=limit_count]').val());

        $(self.containerSelector).on('click', '.sheetMore', function (e) {
            e.preventDefault();
            if (self.lock) {
                return;
            }
            if ($(self.containerSelector).find('input[name=more]').val() == 1) {
                $(self.containerSelector).find('input[name=more]').val(0);
                self.fetch(true);


            } else {
                $(self.containerSelector).find('input[name=more]').val(1);
                self.fetch(true);
            }


        });

        $(self.containerSelector).on('click', '.addComparable', function (e) {
            e.preventDefault;
            if (self.lock) {
                return;
            }
            self.toggleComparableSelect();
        });

        self.bindSelect2();

    };

    this.init();
};