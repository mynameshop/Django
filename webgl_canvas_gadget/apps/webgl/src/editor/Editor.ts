namespace CG {
    export class Editor {
        static Instance: Editor;
        environmentEditor: EnvironmentEditor;
        materialEditor: MaterialEditor;
        lensFlareEditor: LensFlareEditor;
        cardEditor: CardEditor;
        scene: BABYLON.Scene;

        constructor() {
            Editor.Instance = this;
            App.Instance.scene.executeWhenReady(() => {
                this.scene = App.Instance.scene;
                this.environmentEditor = new EnvironmentEditor(App.Instance.scene, App.Instance.environment);
                this.materialEditor = new MaterialEditor(App.Instance.scene, App.Instance.materialManager);
                this.lensFlareEditor = new LensFlareEditor(App.Instance.scene, App.Instance.lensFlareSystem);
                this.cardEditor = new CardEditor(App.Instance.scene, App.Instance.cardManager);

                this.scene.debugLayer.show(window.location.href.indexOf('debug') !== -1);
                this.scene.debugLayer.shouldDisplayLabel = (node) => {
                    return false;
                };

                this.scene.debugLayer.shouldDisplayAxis = (mesh) => {
                    return false;
                };

                // revert optimizations that are client only
                this.undoOptimizations();
            });
        }

        private undoOptimizations(): void {
            App.Instance.scene.unfreezeMaterials();
            App.Instance.scene.meshes.forEach(mesh => {
                mesh.unfreezeWorldMatrix();
            });
        }

        save(): string {
            if (this.scene) {
                let json = '{';
                json += '"camera_pos":' + (this.scene ? JSON.stringify(this.scene.activeCamera.position) : '') + ',';
                json += '"id":"' + App.Instance.uploadManager.id + '",';
                json += '"callouts":' + this.cardEditor.toJSON() + ',';
                json += '"materials":' + this.materialEditor.ToJson() + ',';
                json += '"flares":' + this.lensFlareEditor.LensToJSON() + '}';
                return json;
            }
            return '{}';
        }

        takeScreenshot(w: number, h: number): void {
            let size = this.scene.getEngine().getRenderWidth();
            let sizeH = this.scene.getEngine().getRenderHeight();
            this.scene.getEngine().setSize(w, h);
            App.Instance.scene.render();
            BABYLON.Tools.CreateScreenshot(this.scene.getEngine(), this.scene.activeCamera, { width: w, height: h });
            this.scene.getEngine().setSize(size, sizeH);
        }

        takeSC: boolean = false;
        take25D(model_id: number, w: number, h: number, horizontalFrames: number, verticalFrames: number): void {
            if (this.takeSC) {
                this.takeSC = false;
                return;
            }
            let camera = <BABYLON.ArcRotateCamera>App.Instance.scene.activeCamera;
            let verticalBeta = camera.beta / verticalFrames;
            let horizontalAlpha = 2 * Math.PI / horizontalFrames;
            let numH = 1, numV = 1;
            this.takeSC = true;
            let currentAlpha = camera.alpha;
            let currentBeta = camera.beta;
            let result = [];
            App.Instance.scene.registerAfterRender(() => {
                if (this.takeSC) {
                    let s = '';
                    if (numH + (numV - 1) * horizontalFrames < 10) {
                        s += '00';
                    }
                    else if (numH + (numV - 1) * horizontalFrames < 100) {
                        s += '0';
                    }
                    s += numH + (numV - 1) * horizontalFrames;
                    BABYLON.Tools.CreateScreenshot(this.scene.getEngine(), this.scene.activeCamera, { width: w, height: h }, s, function(data){
                    	result.push({
                    		"numh": numH,
                    		"numv": numV,
                    		"data": data,
                    	});
                    }, "image/jpeg");
                    camera.alpha -= horizontalAlpha;
                    numH++;
                    if (numH > horizontalFrames) {
                        numH = 1;
                        numV++;
                        camera.alpha = currentAlpha;
                        camera.beta -= verticalBeta;
                    }
                    if (numV > verticalFrames) {
                    	numV = 1;
                        this.takeSC = false;
                        camera.alpha = currentAlpha;
                        camera.beta = currentBeta;
                        App.Instance.scene.registerAfterRender(() => {});
                        
                        let send_25d_images = function(i: number) {
                        	let r = {};
                        	if(i > -1) {
                        		r = {"image": JSON.stringify(result[i])};
                        	}else {
                        		r = {"clear": true};
                        	}
                        	$.ajax({
					            url: '/projects/model/' + model_id + '/edit/' + 'gallery/',
					            type: 'POST',
					            dataType: 'json',
					            data: r,
					            success: function( data ) {
					            	i++;
					            	console.log(i, '/', result.length)
					            	if(i < result.length) {
					            		send_25d_images(i);
					            	}else {
					            		result = [];
					            	}
					            },
					        });
                        }
                        send_25d_images(-1);
                    }
                }
            });
            App.Instance.scene.render();
        }
    }
}