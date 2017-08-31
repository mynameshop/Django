namespace CG {
    export class UploadManager {
        uploading: boolean = false;
        id: string;

        constructor(public scene: BABYLON.Scene, public env: Environment) {
            $('body').on('modelChanged', (e: any) => {
                if (this.uploading) {
                    return;
                }

                this.uploading = true;
                let paths: string[] = e.model.split('/');
                let mName = paths[paths.length - 1];
                paths.pop();
                this.id = e.id;
                let mPath = paths.join('/');
                mPath += '/';

                if (e.model == null && App.Instance.modelMeshes.length > 0) {
                    for (let i = 0; i < App.Instance.modelMeshes.length; i++) {
                        scene.getMaterialByName(App.Instance.modelMeshes[i].name).dispose();
                        scene.getMeshByName(App.Instance.modelMeshes[i].name).dispose();
                        App.Instance.modelMeshes[i].dispose();
                    }
                    if (env.groundShadow != null) {
                        env.groundShadow.dispose();
                        env.groundShadow = null;
                    }
                    App.Instance.modelMeshes = [];
                }
                // switch on/off camera auto rotation for model
                App.Instance.shouldRotateCamera = e.rotate_camera;
                (<BABYLON.ArcRotateCamera>App.Instance.scene.activeCamera).lowerRadiusLimit = e.camera_min_distance;
                (<BABYLON.ArcRotateCamera>App.Instance.scene.activeCamera).upperRadiusLimit = e.camera_max_distance;

                (<BABYLON.ArcRotateCamera>App.Instance.scene.activeCamera).upperBetaLimit = e.camera_upper_beta_limit;
                // (<BABYLON.ArcRotateCamera>sceneMain.activeCamera).radius = (e.min + e.max) / 2;
                this.uploadNewModel(mPath, mName, scene, env, e.materials, e.default_material, e.flares, e.camera_pos, e.callouts, e.animations);
            });
        }

        uploadNewModel(modelPath: string, modelName: string, scene: BABYLON.Scene, env: Environment, materials: IMaterialJson[], defaultMaterial: IMaterialJson, flares: IFlareJson[], cameraPos: BABYLON.Vector3, callouts: any, animations: IAnimationMetaJson) {
            for (let i = 0; i < App.Instance.lensFlareSystem.mainLensEmitter.length; i++) {
                App.Instance.lensFlareSystem.disposeFlareSystem(0);
            }

            for (let i = 0; i < scene.lensFlareSystems.length; i++) {
                scene.lensFlareSystems[i].dispose();
            }
            scene.lensFlareSystems.splice(0, scene.lensFlareSystems.length);

            while (App.Instance.modelMeshes.length > 0) {
                for (let i = 0; i < App.Instance.modelMeshes.length; i++) {
                    scene.materials.splice(scene.materials.indexOf(scene.getMaterialByName(App.Instance.modelMeshes[i].name)), 1);
                    scene.getMeshByName(App.Instance.modelMeshes[i].name).dispose();
                }
                for (let i = 0; i < App.Instance.modelMeshes.length; i++) {
                    App.Instance.modelMeshes[i] = null;
                }
                if (env.groundShadow != null) {
                    env.groundShadow.dispose();
                    env.groundShadow = null;
                }
                App.Instance.modelMeshes = [];
            }

            let cam = scene.getMeshByName('Camera_Pivot');
            if (cam) {
                cam.dispose();
            }

            BABYLON.SceneLoader.ImportMesh(null, modelPath, modelName, scene, (newMeshes) => {
                let meshLen = newMeshes.length;
                let sourceMaterial = App.Instance.materialManager.getMaterialByName('Matte Finish');
                for (let i = 0; i < meshLen; i++) {
                    newMeshes[i].scaling = new BABYLON.Vector3(0.01, 0.01, 0.01);
                    if (newMeshes[i].name.localeCompare('Camera_Pivot') === 0) {
                        (<BABYLON.ArcRotateCamera>scene.activeCamera).target = newMeshes[i].position;
                        continue;
                    }
                    if (newMeshes[i].name.localeCompare('Ground_Plane') === 0) {
                        Tools.logMessage('Loading Ground Plane');
                        let stdMat: BABYLON.StandardMaterial = <BABYLON.StandardMaterial>scene.getMaterialByName('Ground_Plane_Material');
                        if (!stdMat) {
                            stdMat = new BABYLON.StandardMaterial('Ground_Plane_Material', scene);
                        }
                        scene.getMaterialByName(newMeshes[i].material.name).dispose();
                        if (newMeshes[i].material) {
                            newMeshes[i].material.dispose();
                        }
                        stdMat.diffuseTexture = Tools.getTextureByUrl(modelPath + 'Ground_Plane.png', scene) || new BABYLON.Texture(modelPath + 'Ground_Plane.png', scene);
                        stdMat.opacityTexture = stdMat.diffuseTexture;
                        stdMat.specularColor = BABYLON.Color3.Black();
                        stdMat.diffuseColor = BABYLON.Color3.White();
                        newMeshes[i].isPickable = false;
                        newMeshes[i].material = stdMat;
                        env.groundShadow = <BABYLON.Mesh>newMeshes[i];
                        env.groundShadow.setEnabled(env.groundShadowEnabled);
                        Tools.logMessage('Ground Plane Done');
                        continue;
                    }
                    else if (newMeshes[i].name.indexOf('Component_') > -1) {
                        Tools.logMessage('loading ' + newMeshes[i].name);
                        if (!newMeshes[i].material) {
                            Tools.logMessage('Material is null for component: ' + newMeshes[i].name);
                            continue;
                        }

                        let targetMaterial;
                        let url = modelPath + newMeshes[i].name.substr(0) + '_AO.jpg';
                        let ambTex = Tools.getTextureByUrl(url, scene) || new BABYLON.Texture(url, scene);
                        // if multimaterial
                        if (newMeshes[i].subMeshes.length > 1) {
                            let multiMaterial = new BABYLON.MultiMaterial(newMeshes[i].name, scene);
                            let subLen = newMeshes[i].subMeshes.length;

                            for (let s = 0; s < subLen; s++) {
                                targetMaterial = new BABYLON.PBRMaterial(newMeshes[i].name + '_Sub_' + s, scene);
                                App.Instance.materialManager.copyMaterial(sourceMaterial, targetMaterial);

                                if ((<BABYLON.StandardMaterial>(<BABYLON.MultiMaterial>newMeshes[i].material).subMaterials[s]).diffuseTexture) {
                                    targetMaterial.albedoTexture = (<BABYLON.StandardMaterial>(<BABYLON.MultiMaterial>newMeshes[i].material).subMaterials[s]).diffuseTexture.clone();
                                }
                                targetMaterial.refractionTexture = null;
                                let url = modelPath + newMeshes[i].name.substr(0) + '_AO.jpg';
                                targetMaterial.ambientTexture = ambTex;
                                targetMaterial.ambientTexture.coordinatesIndex = 1;
                                // targetMaterial.useLogarithmicDepth = true;
                                multiMaterial.subMaterials.push(targetMaterial);
                            }
                            targetMaterial = multiMaterial;
                            for (let mm = 0; mm < (<BABYLON.MultiMaterial>newMeshes[i].material).subMaterials.length; mm++) {
                                if (scene.getMaterialByName((<BABYLON.MultiMaterial>newMeshes[i].material).subMaterials[mm].name)) {
                                    scene.getMaterialByName((<BABYLON.MultiMaterial>newMeshes[i].material).subMaterials[mm].name).dispose();
                                }
                            }
                        }
                        else {
                            targetMaterial = new BABYLON.PBRMaterial(newMeshes[i].name, scene);
                            App.Instance.materialManager.copyMaterial(sourceMaterial, targetMaterial);

                            if ((<BABYLON.StandardMaterial>newMeshes[i].material).diffuseTexture) {
                                targetMaterial.albedoTexture = (<BABYLON.StandardMaterial>newMeshes[i].material).diffuseTexture.clone();
                            }
                            targetMaterial.refractionTexture = null;
                            targetMaterial.ambientTexture = ambTex;
                            targetMaterial.ambientTexture.coordinatesIndex = 1;
                            // targetMaterial.useLogarithmicDepth = true;
                            scene.getMaterialByName(newMeshes[i].material.name).dispose();
                        }

                        if ((<BABYLON.StandardMaterial>newMeshes[i].material)) {
                            (<BABYLON.StandardMaterial>newMeshes[i].material).dispose();
                        }

                        newMeshes[i].material = targetMaterial;
                        App.Instance.modelMeshes.push(newMeshes[i]);
                        Tools.logMessage('loading ' + newMeshes[i].name + ' done');
                    }
                    else {
                        scene.getMeshByName(newMeshes[i].name).dispose();
                    }
                }
                Tools.logMessage('Mesh loaded');

                for (let i = 0; i < scene.meshes.length; i++) {
                    let f = false;
                    for (let j = 0; j < App.Instance.modelMeshes.length; j++) {
                        if (scene.meshes[i] === App.Instance.modelMeshes[j]) {
                            f = true;
                            break;
                        }
                    }
                    scene.meshes[i].isBlocker = f;
                    scene.meshes[i].isPickable = f;
                }
                Tools.logMessage('loading reflection plane');

                let reflMesh = scene.getMeshByName('reflectionPlane');

                if (reflMesh) {
                    let refl = (<BABYLON.StandardMaterial>scene.getMeshByName('reflectionPlane').material).reflectionTexture;
                    if (refl) {
                        (<BABYLON.MirrorTexture>refl).renderList.splice(0, (<BABYLON.MirrorTexture>refl).renderList.length);

                        if (scene.getMeshByName('background')) {
                            (<BABYLON.MirrorTexture>refl).renderList.push(scene.getMeshByName('background'));
                        }
                        if (scene.getMeshByName('skybox')) {
                            (<BABYLON.MirrorTexture>refl).renderList.push(scene.getMeshByName('skybox'));
                        }
                        for (let i = 0; i < App.Instance.modelMeshes.length; i++) {
                            (<BABYLON.MirrorTexture>refl).renderList.push(App.Instance.modelMeshes[i]);
                        }
                    }
                }
                App.Instance.environment.setReflection(scene);
                Tools.logMessage('reflection plane done');

                if (materials) {
                    App.Instance.materialManager.newModelAdded(materials);
                }

                if (flares) {
                    App.Instance.lensFlareSystem.createFromJson(flares);
                }

                if (callouts) {
                    App.Instance.cardManager.newModelAdded(callouts);
                }

                if (cameraPos) {
                    (<BABYLON.ArcRotateCamera>App.Instance.scene.activeCamera).setPosition(new BABYLON.Vector3(cameraPos.x, cameraPos.y, cameraPos.z));
                }
                if (animations) {
                    App.Instance.animationManager.loadFromJson(animations);
                }

                this.uploading = false;
                App.Instance.scene.executeWhenReady(() => {
                    App.Instance.scene.render();
                });
            }, () => { // progress callback

            }, (scene: BABYLON.Scene, msg: string, exception: any) => { // on error
                console.error('model upload failed: ' + msg + ', exception: ' + exception);
                console.log(exception.stack);
                this.uploading = false;
            });
        }

        applyBumpTextures(): void {
            for (let i = 0; i < this.scene.textures.length; i++) {
                if (this.scene.textures[i].name.indexOf('NORMAL') > -1) {
                    // Component_1_Sub_1_NORMAL
                    let comp = this.scene.textures[i].name.substr(0, this.scene.textures[i].name.indexOf('_NORMAL'));
                    let mat = null;
                    if (comp.indexOf('_Sub_') > -1) {
                    	let mesh = this.scene.getMeshByName(comp.substr(0, comp.indexOf('_Sub')));
                    	mat = (function(subMaterials, id){
                    		for(let i = 0; i < subMaterials.length; i++) {
                    			if(subMaterials[i].id === id) {
                    				return subMaterials[i];
                    			}
                    		}
                    		return undefined;
                    	})(mesh.material.subMaterials, comp);
                    } else {
                        mat = <BABYLON.PBRMaterial>this.scene.getMeshByName(this.scene.textures[i].name.substr(0, this.scene.textures[i].name.indexOf('_NORMAL'))).material;
                    }
                    
                    if(mat) {
	                    mat.bumpTexture = this.scene.textures[i];
	                    mat.invertNormalMapX = true;
	                    mat.invertNormalMapY = true;
                	}
                }
            }
        }

        cleanTexturesArray(): void {
            let i = 0;
            while (i < this.scene.textures.length - 1) {
                let textI = this.scene.textures[i];
                let j = this.scene.textures.length - 1;
                while (j > i) {
                    if (textI.name.indexOf('skybox') === -1 && this.scene.textures[j].getInternalTexture().url && this.scene.textures[j].getInternalTexture().url.localeCompare(textI.getInternalTexture().url) === 0) {
                        for (let m = 0; m < this.scene.materials.length; m++) {
                            if ((<BABYLON.PBRMaterial>this.scene.materials[m]).albedoTexture && (<BABYLON.PBRMaterial>this.scene.materials[m]).albedoTexture.getInternalTexture().url.localeCompare(textI.getInternalTexture().url) === 0) {
                                (<BABYLON.PBRMaterial>this.scene.materials[m]).albedoTexture = textI;
                            }
                        }
                        this.scene.textures[j].dispose();
                        this.scene.textures.splice(j, 1);
                        if (j === this.scene.textures.length) { j--; }
                        continue;
                    }
                    j--;
                }
                i++;
            }
        }
    }
}