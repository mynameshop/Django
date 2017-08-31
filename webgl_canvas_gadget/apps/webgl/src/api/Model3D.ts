namespace CG {
	
	export interface IModel3D {
        id: number;
		file: string;
		default_material: any;
		materials: IMaterialJson[];
		textures: string[];
		callouts: any[];
		flares: any[];
		animation: IAnimationMetaJson;
		thumbnail: any;
		rotate_camera: boolean;
		camera_upper_beta_limit: number;
		camera_max_distance: number;
		camera_min_distance: number;
		camera_pos: BABYLON.Vector3;
		model3dgallery: any[];
	
		get_animations(): any[];
		animate(index: number, onAnimationEnd: (animation) => void, onAnimationError: (str) => void);
    }
	
	export class Model3D implements IModel3D{
		id: number;
		file: string;
		default_material: any;
		materials: IMaterialJson[];
		textures: string[];
		callouts: any[];
		flares: any[];
		animation: IAnimationMetaJson;
		thumbnail: any;
		rotate_camera: boolean;
		camera_upper_beta_limit: number;
		camera_max_distance: number;
		camera_min_distance: number;
		camera_pos: BABYLON.Vector3;
		model3dgallery: any[];
		
		constructor(public project: Project, data: IModel3D) {
			this.id = data.id;
			this.file = data.file;
			this.default_material = data.default_material;
			this.materials = data.materials;
			this.textures = data.textures;
			this.callouts = data.callouts;
			this.flares = data.flares;
			this.animation = data.animation.animations ? data.animation : <IAnimationMetaJson>{"animations": []};
			this.thumbnail = data.thumbnail;
			this.rotate_camera = data.rotate_camera;
			this.camera_upper_beta_limit = data.camera_upper_beta_limit;
			this.camera_max_distance = data.camera_max_distance;
			this.camera_min_distance = data.camera_min_distance;
			this.camera_pos = data.camera_pos;
			
			this.model3dgallery = [];
			for(let i=0; i<data.model3dgallery.length; i++) {
				this.model3dgallery.push('url('+data.model3dgallery[i]+')');
			}
		}
		
		public get_animations(): any[] {
			if(this.project.canvasgadget.webgl_support()) {
				return this.animation.animations;
			}else {
				return [];
			}
		}
		
		public animate(index: number, onAnimationEnd: (animation) => void, onAnimationError: (str) => void) {
			if(!this.project.canvasgadget.webgl_support()) {
				console.warn('Can not animate model without webgl support');
				return;
			}
			if(App.Instance.animationManager.isAnimating){
				console.warn('Another animation is in progress');
				return;
			}
			if(this.project.get_model3d_active_index() == undefined) {
				console.warn('Model is not loaded');
				return;
			}
			if(this.project.model3d_set[this.project.get_model3d_active_index()].id != this.id ) {
				console.warn('Model is not loaded');
				return;
			}
			if(index == undefined || typeof index != 'number' || (index%1) != 0 || index < 0) {
				console.warn('Animation index must be positive integer');
				return;
			}
			if(index >= this.animation.animations.length) {
				console.warn('Animation index is out of range');
				return;
			}
			App.Instance.animationManager.animate(index);
		}
	}
	
}