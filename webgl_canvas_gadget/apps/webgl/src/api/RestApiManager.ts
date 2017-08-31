namespace CG {
	export class RestApiManager {
		
		constructor(){};
		
		private data_loader: RestApiDataLoader = new RestApiDataLoader();
		
		load_project(id: number, onloaded: (data) => void, onerror: (err) => void) {
			this.data_loader.load_project_data(
				id, 
				(data) => {
					if(onloaded) {
						onloaded(JSON.parse(data));
					}
				}, 
				(msg) => {
					console.error(msg);
					if(onerror) {
						onerror(msg)
					}
				}
			);
		}
	}
}