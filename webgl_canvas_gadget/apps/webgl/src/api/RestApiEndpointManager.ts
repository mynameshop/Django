namespace CG {
	export class RestApiEndpointManager {
		private api_domain: string;
		private api_root: string = "api/v1/";
	
		constructor(){}
	
		public getProject(id: number) {
			return `${this.getApiUrlRoot()}project/${id}/?format=json`;
		}
		
		private getApiUrlRoot() {
			return `${this.getScriptDomain()}${this.api_root}`;
		}
		
		private getScriptDomain() {
			if(!this.api_domain) {
				let path = document.querySelector(`script[src*="${this.getScriptName()}"]`).getAttribute("src");
				if(path.indexOf("/") === 0) {
					this.api_domain = "/";
				}else {
					let pref = path.split("//")[0];
					let domain = path.split("//")[1].split("/")[0];
					this.api_domain = `${pref}//${domain}/`;
				}
			}
			return this.api_domain;
		}
		
		private getScriptName() {
		    return "canvasgadget.js";
		}
	
	}
}