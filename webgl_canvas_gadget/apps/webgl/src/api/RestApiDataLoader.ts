namespace CG {
	export class RestApiDataLoader {
		
		private endpoint_manager: RestApiEndpointManager = new RestApiEndpointManager();
	
		constructor() {}
		
		load_project_data(id: number, onloaded: (data) => void, onerror: (msg) => void ) {
			var XHR = (<any>window).XDomainRequest || (<any>window).XMLHttpRequest
			var xhr = new XHR();
			xhr.open("GET", this.endpoint_manager.getProject(id), true);
			xhr.onload = function (e) {
				if (xhr.readyState === 4) {
					if (xhr.status === 200) {
						onloaded(xhr.responseText);
					} else {
						onerror(xhr.statusText);
					}
				}
			};
			xhr.onerror = function (e) {
				onerror(xhr.statusText);
			};
			xhr.send();
		}
	}
}