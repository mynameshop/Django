namespace CG {
	
	export class CanvasGadget {
		
		private project : Project;
		private restapi: RestApiManager = new RestApiManager();
		
		constructor(public canvas: HTMLCanvasElement = (<HTMLCanvasElement>document.getElementById('cgRenderCanvas'))) {
			this.canvas = canvas;
		}
		
		public load_project(id: number, onloaded: (obj) => void, onerror: (err) => void) {
			this.restapi.load_project(
				id, 
				(data) => {
					if(this.project) {
						delete this.project;
					}
					this.project = new Project(this, data);
					if(this.webgl_support()) {
						if(App.Instance) {
							delete App.Instance;
						}
						let app = new App(
							this.canvas, 
							this.project, 
							() => {
								if(onloaded){
									onloaded(this.project);
								}
							}
						);
					}else {
						if(onloaded){
							onloaded(this.project);
						}
					}
				}, 
				(err) => {
					if(onerror) {
						onerror(err)
					}
				}
			);
		}
		
		public webgl_support(): boolean {
			try{
				var gl = this.canvas.getContext( 'webgl' ) || this.canvas.getContext( 'experimental-webgl' );
				return (gl && gl instanceof WebGLRenderingContext);
			}catch( e ) { 
				return false; 
			} 
		}
		
	}
	
}