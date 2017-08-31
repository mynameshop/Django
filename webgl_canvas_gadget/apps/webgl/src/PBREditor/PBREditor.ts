namespace CG {
    export class PBREditor {
        gui: any;
        oldPos: BABYLON.Vector3;
        constructor() {
            let meshes: BABYLON.AbstractMesh[] = [];
            let canvas = <HTMLCanvasElement>document.getElementById('renderCanvas');
            let engine = new BABYLON.Engine(canvas, true);
            this.gui = new dat.GUI();
            let scene = new BABYLON.Scene(engine);
            let camera = new BABYLON.FreeCamera('Camera', new BABYLON.Vector3(0, 30, 30), scene);
            camera.setTarget(BABYLON.Vector3.Zero());
            camera.attachControl(canvas, false);
            scene.activeCamera = camera;
            scene.clearColor = BABYLON.Color3.Gray();
            // Light
            let hemilight = new BABYLON.HemisphericLight('hemilight', new BABYLON.Vector3(0, 1, 0), scene);
            hemilight.range = 1;
            hemilight.intensity = 1;
            // Environment Texture
            let hdrTexture = new BABYLON.CubeTexture('./skybox/skybox', scene);
            // Skybox
            let hdrSkybox = BABYLON.Mesh.CreateBox('hdrSkyBox', 1000.0, scene);
            let hdrSkyboxMaterial = new BABYLON.PBRMaterial('skyBox', scene);
            hdrSkyboxMaterial.backFaceCulling = false;
            hdrSkyboxMaterial.reflectionTexture = hdrTexture.clone();
            hdrSkyboxMaterial.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
            hdrSkyboxMaterial.microSurface = .99;
            hdrSkyboxMaterial.cameraExposure = 0.6;
            hdrSkyboxMaterial.cameraContrast = 1.6;

            hdrSkybox.material = hdrSkyboxMaterial;
            hdrSkybox.infiniteDistance = true;

            let meshMaterial = new BABYLON.PBRMaterial('mat', scene);
            meshMaterial.reflectivityColor = BABYLON.Color3.Black();
            this.displayMaterialValues(meshMaterial, scene);
            meshMaterial.reflectionTexture = hdrTexture;

            {
                let Sphere = BABYLON.Mesh.CreateSphere('Sphere', 100, 6, scene, true);
                Sphere.material = meshMaterial;
                Sphere.position.addInPlace(new BABYLON.Vector3(8, 0, 0));
                meshes.push(Sphere);
            }

            {
                let Cube = BABYLON.Mesh.CreateBox('Cube', 6, scene, true);
                Cube.material = meshMaterial;
                Cube.position.addInPlace(new BABYLON.Vector3(0, 0, 0));
                meshes.push(Cube);
            }

            {
                let Plane = BABYLON.Mesh.CreatePlane('Plane', 6, scene, true);
                Plane.material = meshMaterial;
                Plane.position.addInPlace(new BABYLON.Vector3(-8, 0, 0));
                Plane.rotate(new BABYLON.Vector3(1, 0, 0), 1.5708);
                meshes.push(Plane);
            }
            let txtAre = document.getElementById('txt');
            let btn = document.getElementById('btn');
            btn.onclick = (ev) => {
                let txt = '[';
                for (let i = 0; i < scene.meshes.length; i++) {
                    if (scene.meshes[i].material instanceof BABYLON.PBRMaterial && scene.meshes[i].material.name !== 'skyBox') {
                        txt += this.generateJson(<BABYLON.PBRMaterial>scene.meshes[i].material, false);
                        txt += ',';
                    }
                }

                txt = txt.substr(0, txt.length - 2);
                txt += ']';
                txtAre.textContent = txt;
            };

            document.getElementById('groundImg').onchange = (e) => this.updateTexture(scene);
            engine.runRenderLoop(() => {
                scene.render();
            });

            window.addEventListener('resize', () => {
                engine.resize();
            });
        }
        generateJson(pbr: BABYLON.PBRMaterial, display: boolean): string {
            let txt = '{' +
                '"name":"' + pbr.name + '",' +
                '"isGlass":"' + (pbr.refractionTexture ? 'true' : 'false') + '",' +
                '"indexOfRefraction":' + pbr.indexOfRefraction.toPrecision(2) + ',' +
                '"alpha":' + pbr.alpha.toPrecision(2) + ',' +
                '"directIntensity":' + pbr.directIntensity.toPrecision(2) + ',' +
                '"emissiveIntensity":' + pbr.emissiveIntensity.toPrecision(2) + ',' +
                '"environmentIntensity":' + pbr.environmentIntensity.toPrecision(2) + ',' +
                '"specularIntensity":' + pbr.specularIntensity.toPrecision(2) + ',' +
                '"overloadedShadowIntensity":' + pbr.overloadedShadowIntensity.toPrecision(2) + ',' +
                '"overloadedShadeIntensity":' + pbr.overloadedShadeIntensity.toPrecision(2) + ',' +
                '"cameraExposure":' + pbr.cameraExposure.toPrecision(2) + ',' +
                '"cameraContrast":' + pbr.cameraContrast.toPrecision(2) + ',' +
                '"microSurface":' + pbr.microSurface.toPrecision(2) + ',' +
                '"reflectivityColor":{"r":' + pbr.reflectivityColor.r.toPrecision(2) + ', "g":' + pbr.reflectivityColor.g.toPrecision(2) + ', "b":' + pbr.reflectivityColor.b.toPrecision(2) + '}' +
                '}';

            if (display) {
                let txtAre = document.getElementById('txt');
                let btn = document.getElementById('btn');
                txtAre.textContent = txt;
            }

            return txt;
        }

        displayMaterialValues(material: BABYLON.PBRMaterial, scene: BABYLON.Scene) {
            let folder = this.gui.addFolder(material.name);
            let name = folder.add(material, 'name').listen();
            name.onFinishChange((value: string) => {
                if (value.indexOf('{') > -1) {
                    let jsonMat = JSON.parse(value);

                    material.name = jsonMat.name;
                    material.indexOfRefraction = jsonMat.indexOfRefraction;
                    material.alpha = jsonMat.alpha;
                    material.directIntensity = jsonMat.directIntensity;
                    material.emissiveColor = jsonMat.emissiveColor;
                    material.emissiveIntensity = jsonMat.emissiveIntensity;
                    material.environmentIntensity = jsonMat.environmentIntensity;
                    material.specularIntensity = jsonMat.specularIntensity;
                    material.overloadedShadowIntensity = jsonMat.overloadedShadowIntensity;
                    material.overloadedShadeIntensity = jsonMat.overloadedShadeIntensity;
                    material.cameraExposure = jsonMat.cameraExposure;
                    material.cameraContrast = jsonMat.cameraContrast;
                    material.microSurface = jsonMat.microSurface;
                    material.reflectivityColor = new BABYLON.Color3(jsonMat.reflectivityColor.r, jsonMat.reflectivityColor.g, jsonMat.reflectivityColor.b);
                }
            });
            folder.add(material, 'indexOfRefraction', 0, 2).listen();
            folder.add(material, 'alpha', 0, 1).listen();
            folder.add(material, 'directIntensity', 0, 2).listen();
            let emissive = folder.addColor(material, 'emissiveColor').listen();
            emissive.onChange((value) => {
                material.emissiveColor = new BABYLON.Color3(value.r / 255.0, value.g / 255.0, value.b / 255.0);
            });
            folder.add(material, 'emissiveIntensity', 0, 2).listen();
            folder.add(material, 'environmentIntensity', 0, 2).listen();
            folder.add(material, 'specularIntensity', 0, 2).listen();
            folder.add(material, 'overloadedShadowIntensity', 0, 2).listen();
            folder.add(material, 'overloadedShadeIntensity', 0, 2).listen();
            folder.add(material, 'cameraExposure', 0, 2).listen();
            folder.add(material, 'cameraContrast', 0, 2).listen();
            folder.add(material, 'microSurface', 0, 1).listen();
            let color = folder.addColor(material, 'albedoColor').listen();
            color.onChange((value) => {
                material.albedoColor = new BABYLON.Color3(value.r / 255.0, value.g / 255.0, value.b / 255.0);
            });
            folder.add(material.reflectivityColor, 'r', 0, 1.0).listen();
            folder.add(material.reflectivityColor, 'g', 0, 1.0).listen();
            folder.add(material.reflectivityColor, 'b', 0, 1.0).listen();
            let obj = {
                Generate_Json: () => {
                    let txt = '{' +
                        '"name":"' + material.name + '",' +
                        '"isGlass":"' + (material.refractionTexture ? 'true' : 'false') + '",' +
                        '"indexOfRefraction":' + material.indexOfRefraction.toPrecision(2) + ',' +
                        '"alpha":' + material.alpha.toPrecision(2) + ',' +
                        '"directIntensity":' + material.directIntensity.toPrecision(2) + ',' +
                        // '"emissiveColor":' + JSON.stringify(material.emissiveColor) + ',' +
                        '"emissiveIntensity":' + material.emissiveIntensity.toPrecision(2) + ',' +
                        '"environmentIntensity":' + material.environmentIntensity.toPrecision(2) + ',' +
                        '"specularIntensity":' + material.specularIntensity.toPrecision(2) + ',' +
                        '"overloadedShadowIntensity":' + material.overloadedShadowIntensity.toPrecision(2) + ',' +
                        '"overloadedShadeIntensity":' + material.overloadedShadeIntensity.toPrecision(2) + ',' +
                        '"cameraExposure":' + material.cameraExposure.toPrecision(2) + ',' +
                        '"cameraContrast":' + material.cameraContrast.toPrecision(2) + ',' +
                        '"microSurface":' + material.microSurface.toPrecision(2) + ',' +
                        '"reflectivityColor":{"r":' + material.reflectivityColor.r.toPrecision(2) + ', "g":' + material.reflectivityColor.g.toPrecision(2) + ', "b":' + material.reflectivityColor.b.toPrecision(2) + '}' +
                        '}';

                    let txtAre = document.getElementById('txt');
                    let btn = document.getElementById('btn');
                    txtAre.textContent = txt;
                }
            };

            folder.add(obj, 'Generate_Json');
        }

        updateTexture(scene: BABYLON.Scene) {
            let file = (<File>(<HTMLInputElement>document.querySelector('#groundImg')).files[0]);
            let reader = new FileReader();

            if (file) {
                reader.readAsDataURL(file);
            }
            reader.onloadend = () => {
                console.log(file.name);

                for (let i = 0; i < scene.meshes.length; i++) {
                    let mesh = scene.meshes[i];
                    if ((<BABYLON.PBRMaterial>mesh.material).albedoTexture) {
                        (<BABYLON.PBRMaterial>mesh.material).albedoTexture.dispose();
                    }
                    (<BABYLON.PBRMaterial>mesh.material).albedoTexture = BABYLON.Texture.CreateFromBase64String(reader.result, file.name, scene);
                }
            };
        }
    }
}