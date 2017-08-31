namespace CG {
    export interface IFlareJson {
        id: number;
        pos: BABYLON.Vector3;
        main_flare: string;
        hexigon_shape: string;
        band_1: string;
        band_2: string;
    }
    export class LensFlareSystem {
        mainLensEmitter: BABYLON.Mesh[] = [];
        hexaLensEmitter: BABYLON.Mesh[] = [];
        hexaLensFlareSystem: BABYLON.LensFlareSystem[] = [];
        MainLensFlareSystem: BABYLON.LensFlareSystem[] = [];
        flareSizes: number[] = [];
        ids: number[] = [];
        selectedLens: number;
        observer: BABYLON.Observer<BABYLON.Scene>;

        constructor(private scene: BABYLON.Scene) {
        }

        createFlares(position: BABYLON.Vector3, fpMain: string, fpHexa: string, fpB_1: string, fpB_2: string) {
            this.mainLensEmitter.push(new BABYLON.Mesh('lensEmitter' + this.mainLensEmitter.length, this.scene));
            this.mainLensEmitter[this.mainLensEmitter.length - 1].position = position;
            this.MainLensFlareSystem.push(new BABYLON.LensFlareSystem('mainLensFlareSystem' + this.MainLensFlareSystem.length, this.mainLensEmitter[this.mainLensEmitter.length - 1], this.scene));
            this.mainLensEmitter[this.mainLensEmitter.length - 1].isPickable = false;
            let flare = new BABYLON.LensFlare(.4, 1, new BABYLON.Color3(1, 1, 1), fpMain, this.MainLensFlareSystem[this.MainLensFlareSystem.length - 1]);

            flare.texture.hasAlpha = true;
            flare.texture.getAlphaFromRGB = true;
            this.hexaLensEmitter.push(new BABYLON.Mesh('hexaLensEmitter' + this.hexaLensEmitter.length, this.scene));
            this.hexaLensEmitter[this.hexaLensEmitter.length - 1].isPickable = false;
            this.hexaLensEmitter[this.hexaLensEmitter.length - 1].position = position;
            this.hexaLensFlareSystem.push(new BABYLON.LensFlareSystem('hexaLensFlareSystem' + this.hexaLensFlareSystem.length, this.hexaLensEmitter[this.hexaLensEmitter.length - 1], this.scene));

            let flare1 = new BABYLON.LensFlare(.2, -2.85, new BABYLON.Color3(0.1, 0.05, 0.05), fpHexa, this.hexaLensFlareSystem[this.hexaLensFlareSystem.length - 1]);
            let flare2 = new BABYLON.LensFlare(.1, -2.3, new BABYLON.Color3(0.1, 0.05, 0.05), fpB_2, this.hexaLensFlareSystem[this.hexaLensFlareSystem.length - 1]);
            let flare3 = new BABYLON.LensFlare(.1, -0.5, new BABYLON.Color3(0.1, 0.05, 0.05), fpHexa, this.hexaLensFlareSystem[this.hexaLensFlareSystem.length - 1]);
            let flare4 = new BABYLON.LensFlare(.05, 0, new BABYLON.Color3(0.1, 0.05, 0.05), fpHexa, this.hexaLensFlareSystem[this.hexaLensFlareSystem.length - 1]);
            let flare5 = new BABYLON.LensFlare(.05, 0.4, new BABYLON.Color3(0.1, 0.05, 0.05), fpB_2, this.hexaLensFlareSystem[this.hexaLensFlareSystem.length - 1]);
            let flare6 = new BABYLON.LensFlare(.05, 0.2, new BABYLON.Color3(0.1, 0.05, 0.05), fpB_1, this.hexaLensFlareSystem[this.hexaLensFlareSystem.length - 1]);
            let flare7 = new BABYLON.LensFlare(.05, 0.5, new BABYLON.Color3(0.1, 0.05, 0.05), fpHexa, this.hexaLensFlareSystem[this.hexaLensFlareSystem.length - 1]);

            for (let i = 0; i < this.hexaLensFlareSystem[this.hexaLensFlareSystem.length - 1].lensFlares.length; i++) {
                this.flareSizes.push(this.hexaLensFlareSystem[this.hexaLensFlareSystem.length - 1].lensFlares[i].size);
            }
        }

        public disposeFlareSystem(index: number) {
            if (this.MainLensFlareSystem.length > 0) {
                this.MainLensFlareSystem[index].lensFlares[0].texture.dispose();
                this.MainLensFlareSystem[index].lensFlares[0].texture = null;
                this.MainLensFlareSystem[index].lensFlares = [];
                this.MainLensFlareSystem.splice(index, 1);
            }

            if (this.hexaLensFlareSystem.length > 0) {
                for (let i = 0; i < this.hexaLensFlareSystem[index].lensFlares.length; i++) {
                    let tex = this.hexaLensFlareSystem[index].lensFlares[i].texture;
                    tex.dispose();
                    tex = null;
                }

                this.hexaLensFlareSystem[index].lensFlares = [];
                this.hexaLensFlareSystem[index].dispose();
                this.hexaLensFlareSystem.splice(index, 1);
            }

            if (this.mainLensEmitter.length > 0) {
                this.mainLensEmitter[index].dispose();
                this.mainLensEmitter.splice(index, 1);
            }

            if (this.hexaLensEmitter.length > 0) {
                this.hexaLensEmitter[index].dispose();
                this.hexaLensEmitter.splice(index, 1);
            }

            if (this.flareSizes.length > 0) {
                this.flareSizes.splice(index, 7);
            }

            if (this.ids.length > 0) {
                this.ids.splice(index, 7);
            }

            if (this.observer) {
                this.scene.onBeforeRenderObservable.remove(this.observer);
                this.observer = null;
            }
        }

        public createFromJson(flares: IFlareJson[]) {
            if (!flares) {
                return;
            }

            Tools.logMessage('loading flares');
            for (let i = 0; i < flares.length; i++) {
                this.ids.push(flares[i].id);
                this.createFlares(new BABYLON.Vector3(flares[i].pos.x, flares[i].pos.y, flares[i].pos.z), flares[i].main_flare, flares[i].hexigon_shape, flares[i].band_1, flares[i].band_2);
            }

            if (this.observer === null) {
                this.observer = this.scene.onBeforeRenderObservable.add((eventData: BABYLON.Scene, eventState: BABYLON.EventState) => {
                    for (let i = 0; i < this.MainLensFlareSystem.length; i++) {
                        let vec1 = this.hexaLensEmitter[i].position;
                        let vec2 = this.scene.activeCamera.position;
                        let dot = BABYLON.Vector3.Dot(vec1, vec2);
                        dot = dot / (Math.sqrt(vec1.x * vec1.x + vec1.y * vec1.y + vec1.z * vec1.z) * Math.sqrt(vec2.x * vec2.x + vec2.y * vec2.y + vec2.z * vec2.z));
                        let acos = Math.acos(dot);
                        let angle = acos * 180 / Math.PI;
                        let bb = 0.06 - angle / 1000;
                        if (bb > 0.1) {
                            bb = 0.1;
                        }
                        for (let j = 0; j < this.hexaLensFlareSystem[i].lensFlares.length; j++) {
                            this.hexaLensFlareSystem[i].lensFlares[j].size = this.flareSizes[i * 7 + j] + (1 - (<BABYLON.ArcRotateCamera>this.scene.activeCamera).radius / 6) / 6;
                            if (angle < 45) {
                                this.hexaLensFlareSystem[i].lensFlares[j].color = new BABYLON.Color3(bb, bb, bb);
                            }
                            else {
                                this.hexaLensFlareSystem[i].isEnabled = false;
                            }
                        }
                    }
                });
            }
            Tools.logMessage('flares done');
        }
    }
}