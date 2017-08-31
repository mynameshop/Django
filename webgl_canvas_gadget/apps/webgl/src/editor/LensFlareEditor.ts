namespace CG {
    export class LensFlareEditor {
        constructor(public scene: BABYLON.Scene, public lensSys: LensFlareSystem) {
            $('body').on('lenseflareDropped', (e: any) => {
                let mesh = this.scene.pick(e.x, e.y);
                if (mesh && mesh.hit) {
                    this.lensSys.ids.push(e.model.id);
                    this.lensSys.createFlares(new BABYLON.Vector3(mesh.pickedPoint.x + mesh.getNormal(true).x / 200, mesh.pickedPoint.y + mesh.getNormal(true).y / 200, mesh.pickedPoint.z + mesh.getNormal(true).z / 200), e.model.main_flare, e.model.hexigon_shape, e.model.band_1, e.model.band_2);
                    App.Instance.requestRender();
                }
            });
            $('body').on('flareDeleted', (e: any) => {
                this.lensSys.disposeFlareSystem(e.index);
                App.Instance.requestRender();
            });

            scene.onPointerObservable.add((eventData: BABYLON.PointerInfo, eventState: BABYLON.EventState) => {
                let pos = new BABYLON.Vector2(this.scene.pointerX, this.scene.pointerY);
                for (let i = 0; i < this.lensSys.mainLensEmitter.length; i++) {
                    let p = BABYLON.Vector3.Project(this.lensSys.mainLensEmitter[i].position, BABYLON.Matrix.Identity(), this.scene.getTransformMatrix(), this.scene.activeCamera.viewport.toGlobal(this.scene.getEngine().getRenderWidth(), this.scene.getEngine().getRenderHeight()));
                    if (BABYLON.Vector2.Distance(pos, new BABYLON.Vector2(p.x, p.y)) < 10) {
                        this.lensSys.selectedLens = i;
                        window['flareSelected'](this.ToJSONFromIndex(this.lensSys.selectedLens));
                        return;
                    }
                }
                window['flareSelected'](null);
            }, BABYLON.PointerEventTypes.POINTERUP);
        }

        LensToJSON(): string {
            let json = '[';
            for (let i = 0; i < this.lensSys.MainLensFlareSystem.length; i++) {
                json += '{"pos":' + JSON.stringify(this.lensSys.mainLensEmitter[i].getAbsolutePosition()) + ',';
                json += '"main_flare":"' + this.lensSys.MainLensFlareSystem[i].lensFlares[0].texture.url + '",';
                json += '"hexigon_shape":"' + this.lensSys.hexaLensFlareSystem[i].lensFlares[0].texture.url + '",';
                json += '"band_1":"' + this.lensSys.hexaLensFlareSystem[i].lensFlares[5].texture.url + '",';
                json += '"band_2":"' + this.lensSys.hexaLensFlareSystem[i].lensFlares[1].texture.url + '",';
                json += '"id":' + this.lensSys.ids[i] + '},';
            }
            if (this.lensSys.MainLensFlareSystem.length > 0) {
                json = json.substring(0, json.length - 1);
            }
            json += ']';

            return json;
        }

        ToJSONFromIndex(i: number): JSON {
            let json = '';
            json += '{"pos":' + JSON.stringify(this.lensSys.mainLensEmitter[i].getAbsolutePosition()) + ',';
            json += '"main_flare":"' + this.lensSys.MainLensFlareSystem[i].lensFlares[0].texture.url + '",';
            json += '"hexigon_shape":"' + this.lensSys.hexaLensFlareSystem[i].lensFlares[0].texture.url + '",';
            json += '"band_1":"' + this.lensSys.hexaLensFlareSystem[i].lensFlares[5].texture.url + '",';
            json += '"band_2":"' + this.lensSys.hexaLensFlareSystem[i].lensFlares[1].texture.url + '",';
            json += '"id":' + this.lensSys.ids[i] + ',';
            json += '"index":' + i + '}';

            return JSON.parse(json);
        }
    }
}