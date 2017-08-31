class CanvasGadget{
    constructor(project_json, model_switcher, is_editor){
    	var self = this;
    	this.project_json = project_json;
    	this.model_switcher = model_switcher;
    	new CG.App(project_json);
    	if(is_editor){
    		new CG.Editor();
    	}
    	
    	model_switcher.change();
    	
    	window.addEventListener('message', function(e){
    		var data = JSON.parse(event.data);
    		var fn = self[data['command']];
    		if(typeof fn === 'function') {
    		    fn(data['params']);
    		}
    	}, false);

    }
    
    runAnimation(data){
    	try{
    		CG.App.Instance.animationManager.animate(data['animation_index']);
    	}catch(e){
    		console.log('run animation error', index, e)
    	}
    }
}