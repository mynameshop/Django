namespace CG {
	
	export interface IProject {
        id: number;
		name: string;
		thumbnail: string;
		environment: IEnvironmentJson;
		model3d_set: IModel3D[];
		material_set: IMaterialJson[];
	
		set_model3d_active_index(index: number, onModelReady: (model) => void, onModelError: (str) => void);
		get_model3d_active_index(): number;
    }
	
	export class Project implements IProject{
		id: number;
		name: string;
		thumbnail: string;
		environment: IEnvironmentJson;
		model3d_set: Model3D[] = [];
		material_set: IMaterialJson[];
	
		_model3d_active_index: number;
		_timer_3dgallery: any;
	
		constructor(public canvasgadget: CanvasGadget, data: IProject) {
			this.id = data.id;
			this.name = data.name;
			this.thumbnail = data.thumbnail;
			this.environment = data.environment;
			this.material_set = data.material_set;
			this._model3d_active_index = undefined;
			for(let i=0; i < data.model3d_set.length; i++) {
				this.model3d_set.push(new Model3D(this, data.model3d_set[i]));
			}
		}
		
		public get_model3d_active_index(): number {
			return this._model3d_active_index;
		}
		
		public set_model3d_active_index(index: number, onModelReady: (model) => void, onModelError: (str) => void) {
			if(index == undefined || typeof index != 'number' || (index%1) != 0 || index < 0) {
				console.warn('Model index must be positive integer');
				return;
			}
			if(index >= this.model3d_set.length) {
				console.warn('Model index is out of range');
				return;
			}
			if(index == this._model3d_active_index) {
				console.warn('Model is already active');
				return;
			}
			this._model3d_active_index = index;
			this.render_model3d();
		}
		
		private render_model3d(model?: Model3D) {
			let self = this;
			if(!model && self.get_model3d_active_index() > -1) {
				model = self.model3d_set[this.get_model3d_active_index()];
			}
			if(model){
				if(self.canvasgadget.webgl_support()) {
					App.Instance.uploadManager.loadModel(model);
				}else {
					self.render_model25d(model);
					let start_x = undefined;
					
					self.canvasgadget.canvas.addEventListener('touchmove', function(e) {
						if (e.targetTouches.length == 1) {
						    var touch = e.targetTouches[0];
						    let step = self.canvasgadget.canvas.offsetWidth/(model.model3dgallery.length + 1);
						    if(start_x == undefined) {
								start_x = touch.pageX;
							}
						    let delta = start_x - e.pageX;
							if(delta > step){
								self.rotate_left_model25d(model);
								start_x = e.pageX;
							}else if(delta < -step) {
								self.rotate_right_model25d(model);
								start_x = e.pageX;
							}
						}
					});
					
					self.canvasgadget.canvas.onmousemove = function(e) {
						function isLeftButton(evt) {
						    evt = evt || window.event;
						    if ('buttons' in evt) {
						        return evt.buttons == 1;
						    }
						    var button = evt.which || evt.button;
						    return button == 1;
						}
						
						if(isLeftButton(e)) {
							let step = self.canvasgadget.canvas.offsetWidth/(model.model3dgallery.length + 1);
							if(start_x == undefined) {
								start_x = e.clientX;
							}
							let delta = start_x - e.clientX;
							if(delta > step){
								self.rotate_left_model25d(model);
								start_x = e.clientX;
							}else if(delta < -step) {
								self.rotate_right_model25d(model);
								start_x = e.clientX;
							}
						}
					};
				}
			}
		}
		
		private render_model25d(model?: Model3D) {
			let self = this;
			if(!model && self.get_model3d_active_index() > -1) {
				model = self.model3d_set[this.get_model3d_active_index()];
			}
			if(model){
				self.canvasgadget.canvas.style.backgroundImage = model.model3dgallery.join(', ');
				self.canvasgadget.canvas.style.backgroundSize = 'cover';
				self.canvasgadget.canvas.style.backgroundPosition = 'center';
				clearInterval(self._timer_3dgallery);
//				self._timer_3dgallery = setInterval(function(){
//					self.rotate_left_model25d(model);
//				}, 68);
			}
		}
		
		private rotate_right_model25d(model?: Model3D) {
			model.model3dgallery.push(model.model3dgallery.shift());
			this.render_model25d(model);
		}
		
		private rotate_left_model25d(model?: Model3D) {
			model.model3dgallery.unshift(model.model3dgallery.pop());
			this.render_model25d(model);
		}
	}
	
}