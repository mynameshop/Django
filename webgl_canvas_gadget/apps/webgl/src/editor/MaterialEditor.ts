namespace CG {
    export class MaterialEditor {
        constructor(scene: BABYLON.Scene, public matMng: MaterialManager) {
            $('body').on('materialDropped', (e: any) => {
                let pickResult = scene.pick(e.x, e.y);

                if (pickResult.hit) {
                    this.matMng.ApplyMaterialToMesh(e.name, pickResult.pickedMesh.name, pickResult.pickedMesh.subMeshes.length > 1 ? pickResult.subMeshId : -1);
                    App.Instance.requestRender();
                }
            });
        }

        public ToJson(): string {
            let json = '[';
            let multi = false;
            let modelMeshes = App.Instance.modelMeshes;
            for (let i = 0; i < modelMeshes.length; i++) {
                let multiMat = modelMeshes[i].subMeshes.length > 1;
                multi = multiMat || multi ? true : false;

                for (let j = 0; j < modelMeshes[i].subMeshes.length; j++) {
                    let compName = modelMeshes[i].name + (multiMat ? '_Sub_' + j : '');
                    let matName = this.matMng.getComponentMaterial(compName);
                    json += '{"name":"' + matName + '","compNum":' + modelMeshes[i].name.substring(10, modelMeshes[i].name.length) + ',"subCompNum":' + (multiMat ? j : -1)
                        + ',"id":"' + this.matMng.getMaterialByName(matName).id + '","thumbnail":"' + this.matMng.getMaterialByName(matName).thumbnail + '"},';
                }
            }
            if (modelMeshes.length > 0 || multi) {
                json = json.substring(0, json.length - 1);
            }
            json += ']';
            return json;
        }
    }
}