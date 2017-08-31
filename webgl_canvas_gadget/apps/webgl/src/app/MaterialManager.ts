namespace CG {
    export class MaterialManager {
        private materials: { [key: string]: Material; } = {};
        private currentComponentMaterial: { [key: string]: string; } = {};
        constructor(materials: IMaterialJson[], private scene: BABYLON.Scene) {
            for (let i = 0; i < materials.length; i++) {
                this.materials[materials[i].name] = new Material(materials[i], scene);
                this.materials[materials[i].name].id = materials[i].id;
            }
            this.currentComponentMaterial = {};
        }

        public copyMaterial(sourceMaterial: Material, targetMaterial: BABYLON.PBRMaterial): void {
        	if (targetMaterial.alpha === 0) {
            	//если объект был невидимым, то не меняем видимость
        		targetMaterial.alpha = 0;
            	targetMaterial.overloadedShadeIntensity = 0;
            	targetMaterial.specularIntensity = 0;
            	targetMaterial.environmentIntensity = 0;
            	targetMaterial.cameraExposure = 0;
            	targetMaterial.cameraContrast = 0;
            	targetMaterial.indexOfRefraction = 0;
            	targetMaterial.emissiveIntensity = 0;
            	targetMaterial.microSurface = 0;   
            	targetMaterial.overloadedShadowIntensity = 0;
            	targetMaterial.directIntensity = 0;
            	targetMaterial.reflectivityColor = new BABYLON.Color3(0, 0, 0);
        		return
            }
        	targetMaterial.alpha = sourceMaterial.alpha;
            targetMaterial.albedoColor = BABYLON.Color3.White();
            targetMaterial.indexOfRefraction = sourceMaterial.indexOfRefraction;
            targetMaterial.directIntensity = sourceMaterial.directIntensity;
            targetMaterial.emissiveIntensity = sourceMaterial.emissiveIntensity;
            targetMaterial.environmentIntensity = sourceMaterial.environmentIntensity;
            targetMaterial.specularIntensity = sourceMaterial.specularIntensity;
            targetMaterial.overloadedShadowIntensity = sourceMaterial.overloadedShadowIntensity;
            targetMaterial.overloadedShadeIntensity = sourceMaterial.overloadedShadeIntensity;
            targetMaterial.cameraExposure = sourceMaterial.cameraExposure;
            targetMaterial.cameraContrast = sourceMaterial.cameraContrast;
            targetMaterial.microSurface = sourceMaterial.microSurface;
            targetMaterial.reflectivityColor = new BABYLON.Color3(sourceMaterial.reflectivityColor.r, sourceMaterial.reflectivityColor.g, sourceMaterial.reflectivityColor.b);
            if (sourceMaterial.normal_map) {
                targetMaterial.bumpTexture = new BABYLON.Texture(sourceMaterial.normal_map, this.scene);
            }else {
                targetMaterial.bumpTexture = null;
            }
        }

        public newModelAdded(json: IMaterialJson[]): void {
            if (!json) {
                return;
            }
            Tools.logMessage('loading materials');

            for (let i = 0; i < json.length; i++) {
                let animJson = json[i];
                this.ApplyMaterialToMesh(animJson.name, 'Component_' + animJson.compNum, json[i].subCompNum);
            }

            Tools.logMessage('materials done');
        }

        public ApplyMaterialToMesh(materialName: string, meshName: string, subCompNum: number): void {
            let mMesh = this.scene.getMeshByName(meshName);
            if (mMesh !== null) {
                let targetMaterial = (<any>mMesh.material);
                if (targetMaterial.subMaterials) {
                    targetMaterial = targetMaterial.subMaterials[ subCompNum ];
                }
                this.copyMaterial(this.getMaterialByName(materialName), targetMaterial);
                targetMaterial.refractionTexture = <any>this.materials[materialName].isGlass ? (<BABYLON.PBRMaterial>mMesh.material).reflectionTexture : null;
                this.currentComponentMaterial[meshName + ((subCompNum > -1) ? '_Sub_' + subCompNum : '')] = materialName;
            }
        }
        
        public setVisibility(visibility: boolean, meshName: string, subCompNum: number): void {
            let mMesh = this.scene.getMeshByName(meshName);
            
            if (mMesh !== null) {
                let targetMaterial = (<any>mMesh.material);
                if (targetMaterial.subMaterials) {
                    targetMaterial = targetMaterial.subMaterials[ subCompNum ];
                }
                
                const materialName = this.getComponentMaterial(targetMaterial.name);
                const material = this.getMaterialByName(materialName)
                
                if(visibility) {
                	targetMaterial.alpha = material.alpha;
                	this.ApplyMaterialToMesh(materialName, meshName, subCompNum)
                } else {
                	targetMaterial.alpha = 0;
                }
                targetMaterial.refractionTexture = <any>this.materials[materialName].isGlass ? (<BABYLON.PBRMaterial>mMesh.material).reflectionTexture : null;
                this.ApplyMaterialToMesh(materialName, meshName, subCompNum)
            }
        }

        public getMaterialByName(name: string): Material {
            return this.materials[name];
        }

        public getComponentMaterial(componentName: string): string {
            return this.currentComponentMaterial[componentName] || 'Matte Finish';
        }
    }
}