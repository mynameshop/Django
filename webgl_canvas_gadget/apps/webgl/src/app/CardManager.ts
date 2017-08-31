namespace CG {
    export class CardManager {
        cardArray: Card[] = [];
        cardJsons: any[] = [];

        constructor(private scene: BABYLON.Scene) {
            scene.onBeforeRenderObservable.add(() => {
                for (let i = 0; i < this.cardArray.length; i++) {
                    this.cardArray[i].update(scene);
                }
            });

            let canvas = scene.getEngine().getRenderingCanvas();

            let onPointerDown = (evt) => {
                let pickResult = scene.pick(scene.pointerX, scene.pointerY, (mesh) => {
                    for (let i = 0; i < this.cardArray.length; i++) {
                        if (mesh === this.cardArray[i].box || mesh === this.cardArray[i].anchor) {
                            return true;
                        }
                    }

                    return false;
                });
                if (pickResult.hit) {
                    for (let i = 0; i < this.cardArray.length; i++) {
                        if (pickResult.pickedMesh === this.cardArray[i].anchor || pickResult.pickedMesh === this.cardArray[i].box) {
                            if (this.cardArray[i].notResizing === true) {
                                if (this.cardArray[i].maximazed) {
                                    this.cardArray[i].gettingSmaller = true;
                                    this.cardArray[i].gettingBigger = false;
                                    this.cardArray[i].notResizing = false;
                                    this.cardArray[i].maximazed = false;
                                    this.cardArray[i].scalingFactor = 0.05;
                                }
                                if (this.cardArray[i].minimazed) {
                                    this.cardArray[i].gettingSmaller = false;
                                    this.cardArray[i].gettingBigger = true;
                                    this.cardArray[i].notResizing = false;
                                    this.cardArray[i].minimazed = false;
                                    this.cardArray[i].scalingFactor = 0.05;
                                }
                            }
                        }
                    }
                }
            };

            canvas.addEventListener('pointerdown', onPointerDown, false);
            scene.onDispose = () => {
                canvas.removeEventListener('pointerdown', onPointerDown);
            };
        }

        newModelAdded(json: any) {
            while (this.cardArray.length > 0) {
                this.cardArray[0].dispose();
                this.cardArray[0] = null;
                this.cardArray.splice(0, 1);
                this.cardJsons.splice(0, 1);
            }

            if (!json) {
                return;
            }
            Tools.logMessage('loading callouts');
            for (let i = 0; i < json.length; i++) {
                this.cardArray.push(new Card(json[i], this.scene, new BABYLON.Vector3(json[i].pos.x, json[i].pos.y, json[i].pos.z)));
                this.cardJsons.push(JSON.stringify(json[i]));
            }
            Tools.logMessage('callouts done');
        }

        deleteCallout() {
            console.error('delete callout not implemented');
        }
    }
}