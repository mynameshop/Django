var StanceAnswerHelper = function (htmlParser) {
    var self = this;
    this.currentChoice = null;
    this.htmlParser = htmlParser;

    this.setChoiceFilter = function (choice) {
        this.currentChoice = choice;
        $('.stanceList .stance').hide();

        if (choice === 'p') {
            $('.stanceList .stancePro').show();
        } else {
            $('.stanceList .stanceCon').show();
        }

        $('.stanceChoices a.choice').each(function () {
            if ($(this).data('choice') == choice) {
                $(this).addClass('chosen');
            } else {
                $(this).removeClass('chosen');
            }

        });

        $('.stanceModalForm .radioChoice').each(function () {
            if ($(this).val() == choice) {
                $(this).attr('checked', 'checked');
            } else {
                $(this).removeAttr('checked');
            }
        });
    };

    this.loadStanceModal = function (question_id, choice) {
        self.modal.show();
        content = self.modal.getContent();
        $(content).html(AjaxSpinner.makeHtml());
        $.ajax({
            url: '/s/stance_modal',
            data: {
                question_id: question_id,
                choice: choice
            },
            cache: false
        }).always(function (data) {
            content = self.modal.getContent();
            $(content).html(data);
            if (choice) {
                self.setChoiceFilter(choice);
            }
            self.switchStanceMode(1);

            markMentions('.stanceModalContainer .stanceText');
            self.htmlParser.parseEach('.stanceModalContainer .parsable');
            bindMentionsTextarea('.stanceModalFormContainer textarea[name=stance_text]');
            self.modal.resize();
        });
    };

    this.answerTriggerClick = function (element) {
        var
                question_id = $(element).data('question-id'),
                choice = $(element).data('choice')
                ;
        this.current_element = $('#questionitem-' + $(element).data('question-id'));
        self.loadStanceModal(question_id, choice);
    };

    this.switchStanceMode = function (isSelect) {
        $('.stanceChoiceContainer').hide();
        $('.stanceModalFormContainer').hide();
        if (isSelect) {
            $('.stanceChoiceContainer').show();
        } else {
            $('.stanceModalFormContainer').show();
        }
        self.modal.resize();
    };

    this.refreshData = function (data) {
        $(this.current_element).children().find('.question-stance-text').html(data.stance_text);
        mentionToHref($(this.current_element).children().find('.question-stance-text'));
        $(this.current_element).children().find('.answerButton')
                .removeClass('proSelected')
                .removeClass('conSelected');

        var ft = $(this.current_element).find('.forTextual');

        if (data.choice == 'p') {
            $(this.current_element)
                    .children()
                    .find('.answerButton[data-choice=p]')
                    .addClass('proSelected');
            $(ft).html($(ft).data('protext'));
        } else {
            $(this.current_element)
                    .children()
                    .find('.answerButton[data-choice=c]')
                    .addClass('conSelected');
            $(ft).html($(ft).data('context'));
        }

        self.modal.hide();

    };

    this.addRefreshTable = function (id) {
        table = AjaxTableManager.getTable(id);
        if (table) {
            this.refreshAjaxTables.push(table);
        }
    };

    this.selectStance = function (stanceId) {
        $.ajax({
            url: $('.stanceModalContainer').data('stance-set-url'),
            dataType: 'json',
            data: {
                stance_id: stanceId
            }
        }).done(function (data) {
            if (data.ok) {
                self.refreshData(data);
            }
        });
    };

    this.setErrors = function (errors) {
        var errorsContainer = $('.stanceModalForm .formErrors');
        errorsContainer.html('');
        for (var i in errors) {
            errorsContainer.append('<div>' + errors[i] + '</div>');
        }
    };

    this.makeStance = function (formElement) {
        $('.stanceModalForm .formErrors').html('');
        $.ajax({
            url: $(formElement).attr('action'),
            method: $(formElement).attr('method'),
            data: $(formElement).serialize()
        }).done(function (data) {
            if (data.ok) {
                self.refreshData(data);
            } else {
                self.setErrors(data.errors);
            }
        });
    };

    this.reloadStances = function (col) {
        var list = $('.stanceModalContainer .stanceList');
        $.ajax({
            url: list.data('url'),
            data: {
                sort_col: col,
                question_id: $('.stanceModalContainer').data('question-id')
            }
        }).always(function (data) {
            $(list).html(data);
            var chosen = $('.stanceChoices a.choice.chosen');

            if (chosen) {
                $(chosen).click();
            }
            
            markMentions('.stanceModalContainer .stanceText');

        });
    };

    this.init = function () {
        this.modal = new Modal();
        this.modal.makeContentContainer('stanceModal');

        $(document).on('click', '.question-answer-trigger', function (e) {
            e.preventDefault();
            if ($('#q-is-user').val()=='0') {
                window.location.href='/login?next=/q';
            } else {
                self.answerTriggerClick(this);
            }
            
        });

        $(document).on('click', '.stanceModalContainer .choice', function (e) {
            e.preventDefault();
            self.setChoiceFilter($(this).data('choice'));
        });

        $(document).on('click', '.stanceModalContainer .switchWrite', function (e) {
            e.preventDefault();
            self.switchStanceMode($(this).data('select'));
        });

        $(document).on('click', '.stanceModalContainer .selectStance', function (e) {
            e.preventDefault();
            self.selectStance($(this).data('stance-id'));
        });

        $(document).on('submit', '.stanceModalForm', function (e) {
            e.preventDefault();
            self.makeStance($(this));
        });

        $(document).on('click', '.stanceModalForm .radioChoice', function () {
            self.setChoiceFilter($(this).val());
        });

        $(document).on('click', '.stanceModalContainer .stanceSorting a', function (e) {
            e.preventDefault();
            self.reloadStances($(this).data('col'));
        });
    };

    this.init();
};