var Modal = function (modalContentId) {
    if (modalContentId) {
        this.setContent(modalContentId, true);
    }
};

Modal.prototype.makeContentContainer = function (additionalClass) {
  content = document.createElement('div');
  content.classList.add('modal');
  if(additionalClass) {
      content.classList.add(additionalClass);
  }
  content.innerHTML = "";
  $('body').append(content);
  this.setContent(content);
};

Modal.prototype.getContent = function () {
    return this.modalContent;
};

Modal.prototype.setContent = function (modalContent, byId) {

    if (byId) {
        console.log('byId');
        this.modalContent = document.getElementById(modalContent);
    } else {
        this.modalContent = modalContent;
    }

    this.overlay = null;
    this.make();
    this.bind();
};

Modal.prototype.bind = function () {
    var self = this;
    this.overlay.addEventListener('click', function (e) {
        self.hide();
    });
    window.addEventListener('resize', function (e) {
       self.resize(); 
    });
};

 
Modal.prototype.resize = function () {
    this.ow = Math.max(document.body.clientWidth, window.innerWidth || 0);
    this.oh = Math.max(document.body.clientHeight, window.innerHeight || 0);
    this.w = this.ow;

    this.h= document.body.clientHeight;

    this.cw = this.modalContent.clientWidth;
    this.ch = this.modalContent.clientHeight;
    this.overlay.style.width = this.ow + 'px';
    this.overlay.style.height = this.oh + 'px';
    this.modalContent.style.left = (this.w/2 - this.cw/2) + 'px';


    var topLocation = (window.outerHeight/2 - this.ch/2)

    if(topLocation+this.ch>window.outerHeight) {
        topLocation = 10;
    } 
    
    this.modalContent.style.top = topLocation + 'px';
   //console.log(this.h, this.ch, this.oh, window.outerHeight);


};

Modal.prototype.makeOverlay = function () {
    var
            overlay = document.getElementById('modal-overlay')
            ;

    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'modal-overlay';
        document.body.appendChild(overlay);
    }

    this.overlay = overlay;
    this.hide();
};

Modal.prototype.make = function () {
    this.makeOverlay();
};

Modal.prototype.show = function () {
    
    this.overlay.style.display = 'block';
    this.modalContent.style.display = 'block';
    this.resize();
    document.body.classList.add('noscroll');

};

Modal.prototype.hide = function () {
    this.overlay.style.display = 'none';
    this.modalContent.style.display = 'none';
    document.body.classList.remove('noscroll');
};



