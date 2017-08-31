namespace CG {
    export interface ICalloutJson {
        x: number;
        y: number;
        pos: any;
    }

    export class CardEditor {
        constructor(public scene: BABYLON.Scene, public cardMng: CardManager) {
            this.scene = scene;
            this.cardMng = cardMng;
        }

        addCallout(jsonData: ICalloutJson): ICalloutJson {
            let mesh = this.scene.pick(jsonData.x, jsonData.y);
            if (mesh && mesh.hit) {
                this.cardMng.cardArray.push(new Card(jsonData, this.scene, new BABYLON.Vector3(mesh.pickedPoint.x + mesh.getNormal(true).x / 200, mesh.pickedPoint.y + mesh.getNormal(true).y / 200, mesh.pickedPoint.z + mesh.getNormal(true).z / 200)));

                let card = <Card>this.cardMng.cardArray[this.cardMng.cardArray.length - 1];
                jsonData.pos = card.box.position;
                this.cardMng.cardJsons.push(JSON.stringify(jsonData));
                return jsonData;
            }
            return jsonData;
        }

        toJSON(): string {
            let json = '[';
            for (let i = 0; i < this.cardMng.cardJsons.length; i++) {
                let s = this.cardMng.cardJsons[i];
                if (s.charAt(0) === '[') {
                    s = s.substring(1, s.length - 1);
                }
                json += s + ',';
            }

            if (this.cardMng.cardJsons.length > 0) {
                json = json.substring(0, json.length - 1);
            }

            json += ']';
            return json;
        }
    }
}