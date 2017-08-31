function UserDropDown(dd) {
    var self = this;
    this.shown = false;



    if (dd.length == 0) {
        return;
    } else {
        this.dd = dd[0];
    }

    this.originalClasses = this.dd.className;

    this.dd.addEventListener('click', function (e) {

        if (e.target.parentNode.className != self.dd.className) {
            return;
        }
        
        e.preventDefault();
        e.stopImmediatePropagation();
        
        if (self.shown) {
            self.hideMenu();
        } else {
            self.showMenu();
        }
        
    });

    document.addEventListener('click', function (e) {
        self.hideMenu();
    });

    this.showMenu = function () {
        if (this.shown) {
            return;
        }
        this.shown = true;
        this.dd.className += " shown";
    };

    this.hideMenu = function () {
        
        if (!this.shown) {
            return;
        }
        this.shown = false;
        this.dd.className = this.originalClasses;
    };

}

window.addEventListener('load', function () {
    var menu = document.getElementById('main-nav').getElementsByClassName("dropdown");
    var profile_switch = document.getElementsByClassName("profile-switch");
    new UserDropDown(menu);
    new UserDropDown(profile_switch);
});

