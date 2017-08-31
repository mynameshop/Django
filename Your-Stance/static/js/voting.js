var Voting = {
    groupsCollection: null,
    setVoteCount: function (group, classname, count) {
        el = group.getElementsByClassName(classname);
        if (el.length > 0) {
            el[0].innerHTML = count;
        }
    },
    updateVotes: function (group, data) {
        Voting.setVoteCount(group, 'votes-pro', data.p_votes);
        Voting.setVoteCount(group, 'votes-against', data.c_votes);
    },
    markSelected: function (element, group) {
        var triggers = group.getElementsByClassName('question-answer-trigger');

        for (var i = 0; i < triggers.length; i++) {
            triggers[i].classList.remove('selected');
        }

        if (!element.classList.hasOwnProperty('question-undecided-trigger')) {
            element.classList.add('selected');
            element.blur();
        }

    },
    voteSuccess: function (element, group, data) {
        data = JSON.parse(data);
        if (data.ok) {
            Voting.markSelected(element, group);
            Voting.updateVotes(group, data);
            
            if (element.getAttribute('data-show-stance')) {
                id = 'stance-trigger-'+element.getAttribute('data-question-id');
                trigger = document.getElementById(id);
                if(trigger) {
                    trigger.click();    
                }
            }
        }
    },
    voteError: function (data) {
        alert('server error');
        console.log(data);
    },
    vote: function (element) {
        var group = Voting.groupsCollection[element.getAttribute('data-group-i')];



        AjaxHelper.commence(element.href, 'GET', function (data) {
            Voting.voteSuccess(element, group, data);
        }, Voting.voteError);

        return false;
    },
    bind: function () {
        Voting.groupsCollection = document.getElementsByClassName("question-btngroup");

        for (var i = 0; i < Voting.groupsCollection.length; i++) {
            triggersCollection = Voting.groupsCollection[i].getElementsByClassName('question-answer-trigger');


            for (var n = 0; n < triggersCollection.length; n++) {

                triggersCollection[n].setAttribute('data-group-i', i);
                triggersCollection[n].addEventListener('click', function (e) {
                    e.preventDefault();
                    Voting.vote(this);
                });

            }
        }
    }

};


//document.addEventListener("DOMContentLoaded", function () {
//    Voting.bind();
//});

