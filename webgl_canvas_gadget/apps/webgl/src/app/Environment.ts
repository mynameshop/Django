namespace CG {
    export interface ITexture {
        id: number;
        url: string;
    }

    export interface IVector3 {
        x: number;
        y: number;
        z: number;
    }

    export interface IColor3 {
        r: number;
        g: number;
        b: number;
    }

    class BabylonLightType {
        static HemisphericLight = 'HemisphericLight';
        static DirectionalLight = 'DirectionalLight';
        static PointLight = 'PointLight';
        static SpotLight = 'SpotLight';
    }

    export interface IBabylonLight {
        type: BabylonLightType;
        position: IVector3;
        direction: IVector3;
        range: number;
        intensity: number;
        diffuse: IColor3;
        specular: IColor3;
        groundColor: IColor3;
        angle: number;
        exponent: number;
    }

    export interface IEnvironmentJson {
        is_editor: boolean;
        show_background: boolean;
        gradient_top_lightness: number;
        gradient_top_hue: number;
        gradient_bottom_lightness: number;
        gradient_bottom_hue: number;
        gradient_offset: number;
        show_ground_plane: boolean;
        ground_plane_scale: number;
        ground_plane: ITexture;
        show_reflective: boolean;
        reflective_amount: number;
        show_shadow: boolean;
        skybox: ITexture;
        light: IBabylonLight[];
    }

    export class Environment {
        backgroundMesh: BABYLON.Mesh;

        skyboxTexture: BABYLON.CubeTexture;
        reflectionTexture: BABYLON.CubeTexture;

        groundMesh: BABYLON.Mesh;
        groundTexture: BABYLON.Texture;
        groundShadow: BABYLON.Mesh;
        groundShadowEnabled: boolean;
        reflectiveMesh: BABYLON.Mesh;
        hueT: number;
        ligthnessT: number;
        saturationT: number;
        hueB: number;
        ligthnessB: number;
        saturationB: number;
        gradientOffset: number;

        constructor(envJson: IEnvironmentJson, scene: BABYLON.Scene) {
            if (!envJson) { return; }

            this.createCameras(scene);
            this.createLight(envJson, scene);

            BABYLON.SceneLoader.ImportMesh('', 'https://canvasgadget.com/static/js/lib/', 'environment.babylon', scene, (meshes) => {
                for (let i = 0; i < meshes.length; i++) {
                    switch (meshes[i].name) {
                        case 'background': this.createBackground(envJson, meshes[i], scene); break;
                        case 'groundPlane': this.createGroundPlane(envJson, meshes[i], scene); break;
                        case 'reflectionPlane': this.createReflectionPlane(envJson, meshes[i], scene); break;
                        default: break;
                    }
                }

                this.groundTexture = null;
                this.groundShadow = <BABYLON.Mesh>scene.getMeshByName('Ground_Plane');
                this.groundShadowEnabled = envJson.show_shadow;

                this.createSkybox(envJson, scene);
                this.createMirror(envJson, meshes, scene);
            });
        }

        private createCameras(scene: BABYLON.Scene) {
            let arcRotate = new BABYLON.ArcRotateCamera('Camera', 0, 0, 6, new BABYLON.Vector3(0, .5, 0), scene);
            arcRotate.lowerRadiusLimit = 1.5;
            arcRotate.upperRadiusLimit = 6;
            arcRotate.upperBetaLimit = 1.5;
            arcRotate.wheelPrecision = 50;
            arcRotate.minZ = 0.1;
            arcRotate.maxZ = 100;
            arcRotate.panningSensibility = 0;
            arcRotate.pinchPrecision = 200;
            scene.activeCamera = arcRotate;
            arcRotate.attachControl(scene.getEngine().getRenderingCanvas(), false, false);

            let arcRotateVR = new BABYLON.VRDeviceOrientationArcRotateCamera('VR', 0, 0, 6, new BABYLON.Vector3(0, .5, 0), scene, true);
            arcRotateVR.lowerRadiusLimit = 1.5;
            arcRotateVR.upperRadiusLimit = 6;
            arcRotateVR.upperBetaLimit = 1.5;
            arcRotateVR.wheelPrecision = 50;
            arcRotateVR.minZ = 0.1;
            arcRotateVR.maxZ = 100;
            arcRotateVR.panningSensibility = 0;
            arcRotateVR.pinchPrecision = 200;
            // scene.activeCamera = arcRotateVR;
            arcRotateVR.attachControl(scene.getEngine().getRenderingCanvas(), false, false);
        }

        private createLight(envJson: IEnvironmentJson, scene: BABYLON.Scene) {
            for (let i = 0; i < envJson.light.length; i++) {
                let light_source = envJson.light[i];
                if (!light_source.position) {
                    continue;
                }
                let light_obj;
                let name = 'light' + i;
                let position = new BABYLON.Vector3(light_source.position.x, light_source.position.y, light_source.position.z);

                if (light_source.type === BabylonLightType.HemisphericLight) {
                    light_obj = new BABYLON.HemisphericLight(name, position, scene);
                }else if (light_source.type === BabylonLightType.DirectionalLight && light_source.direction) {
                    let direction = new BABYLON.Vector3(light_source.direction.x, light_source.direction.y, light_source.direction.z);
                    light_obj = new BABYLON.DirectionalLight(name, direction, scene);
                    light_obj.position = position;
                }else if (light_source.type === BabylonLightType.SpotLight && light_source.direction) {
                    let direction = new BABYLON.Vector3(light_source.direction.x, light_source.direction.y, light_source.direction.z);
                    light_obj = new BABYLON.SpotLight(name, position, direction, light_source.angle || 0.8, light_source.exponent || 2, scene);
                }else if (light_source.type === BabylonLightType.PointLight) {
                    light_obj = new BABYLON.PointLight(name, position, scene);
                }else {
                    continue;
                }

                if (light_source.range) {
                    light_obj.range = light_source.range;
                }
                if (light_source.intensity) {
                    light_obj.intensity = light_source.intensity;
                }
                if (light_source.diffuse) {
                    light_obj.diffuse =  new BABYLON.Color3(light_source.diffuse.r, light_source.diffuse.g, light_source.diffuse.b);
                }
                if (light_source.specular) {
                    light_obj.specular = new BABYLON.Color3(light_source.specular.r, light_source.specular.g, light_source.specular.b);
                }
                if (light_source.groundColor) {
                  light_obj.groundColor = new BABYLON.Color3(light_source.groundColor.r, light_source.groundColor.g, light_source.groundColor.b);
                }
            }
        }

        private createBackground(envJson: IEnvironmentJson, mesh: BABYLON.AbstractMesh, scene: BABYLON.Scene) {
            if (envJson.show_background || envJson.is_editor) {
                mesh.position = new BABYLON.Vector3(0, -0.05, 0);
                this.backgroundMesh = <BABYLON.Mesh>mesh;
                BABYLON.Effect.ShadersStore['gradientVertexShader'] = 'precision highp float;attribute vec3 position;attribute vec2 uv;uniform mat4 worldViewProjection;varying vec2 vUV;void main(void) {gl_Position = worldViewProjection * vec4(position, 1.0);vUV = uv;}';

                BABYLON.Effect.ShadersStore['gradientPixelShader'] = 'precision highp float;varying vec2 vUV;uniform sampler2D textureSampler;uniform float offset;uniform vec3 topColor;uniform vec3 bottomColor;void main(void) {gl_FragColor = vec4(mix(bottomColor, topColor, vUV.y + offset),1);}';

                let shader = new BABYLON.ShaderMaterial('gradient', scene, 'gradient', {});
                this.gradientOffset = envJson.gradient_offset;
                shader.setFloat('offset', envJson.gradient_offset);
                this.saturationT = 1;
                this.saturationB = 1;
                this.ligthnessT = envJson.gradient_top_lightness;
                this.ligthnessB = envJson.gradient_bottom_lightness;
                this.hueT = envJson.gradient_top_hue;
                this.hueB = envJson.gradient_bottom_hue;
                let ints = Tools.hslToRgb(this.hueT, this.saturationT, this.ligthnessT);
                shader.setColor3('topColor', BABYLON.Color3.FromInts(ints[0], ints[1], ints[2]));
                ints = Tools.hslToRgb(this.hueB, this.saturationB, this.ligthnessB);
                shader.setColor3('bottomColor', BABYLON.Color3.FromInts(ints[0], ints[1], ints[2]));
                mesh.material = shader;
                mesh.isPickable = false;
                mesh.setEnabled(envJson.show_background);
                scene.onBeforeRenderObservable.add(() => {
                    this.backgroundMesh.rotation.y = -((<BABYLON.ArcRotateCamera>scene.activeCamera).alpha) + -Math.PI / 2;
                });
            }
            else {
                mesh.dispose();
            }
        }

        private createGroundPlane(envJson: IEnvironmentJson, mesh: BABYLON.AbstractMesh, scene: BABYLON.Scene) {
            if (envJson.show_ground_plane || envJson.is_editor) {
                this.groundMesh = <BABYLON.Mesh>mesh;
                mesh.position = new BABYLON.Vector3(0, -0.03, 0);
                let groundPlaneMaterial = <BABYLON.PBRMaterial>scene.getMaterialByName('groundPlaneMaterial') || new BABYLON.PBRMaterial('groundPlaneMaterial', scene);
                groundPlaneMaterial.albedoTexture = Tools.getTextureByUrl(envJson.ground_plane.url, scene) || new BABYLON.Texture(envJson.ground_plane.url, scene);
                groundPlaneMaterial.opacityTexture = groundPlaneMaterial.albedoTexture;
                groundPlaneMaterial.reflectivityColor = BABYLON.Color3.Black();
                groundPlaneMaterial.overloadedShadeIntensity = 0;
                mesh.material = groundPlaneMaterial;
                mesh.isPickable = false;
                mesh.scaling = new BABYLON.Vector3(envJson.ground_plane_scale, envJson.ground_plane_scale, envJson.ground_plane_scale);
                mesh.setEnabled(envJson.show_ground_plane);
                scene.lights[0].excludedMeshes.push(mesh);
            }
            else {
                mesh.dispose();
            }
        }

        private createReflectionPlane(envJson: IEnvironmentJson, mesh: BABYLON.AbstractMesh, scene: BABYLON.Scene) {
            if (envJson.show_reflective || envJson.is_editor) {
                mesh.position = new BABYLON.Vector3(0, -0.01, 0);
                this.reflectiveMesh = <BABYLON.Mesh>mesh;
                let mirrorMaterial = new BABYLON.StandardMaterial('mirrorMat', scene);
                mirrorMaterial.reflectionTexture = new BABYLON.MirrorTexture('mirrorTexture', 2048, scene, false);
                (<BABYLON.MirrorTexture>mirrorMaterial.reflectionTexture).mirrorPlane = new BABYLON.Plane(0, -1, 0, -0.01);
                mirrorMaterial.reflectionTexture.hasAlpha = true;
                mirrorMaterial.alpha = 0.1;
                mirrorMaterial.diffuseColor = BABYLON.Color3.Black();
                mirrorMaterial.specularColor = BABYLON.Color3.Black();
                mesh.material = mirrorMaterial;
                mesh.scaling = new BABYLON.Vector3(4.9, 1, 4.9);
                mesh.isPickable = false;
                mesh.setEnabled(envJson.show_reflective);
                mesh.material.alpha = envJson.reflective_amount;
                scene.lights[0].excludedMeshes.push(mesh);
            }
            else {
                mesh.dispose();
            }
        }

        private createSkybox(envJson: IEnvironmentJson, scene: BABYLON.Scene) {
            let skyboxCubeTexture = new BABYLON.CubeTexture(envJson.skybox.url + 'skybox', scene);
            this.reflectionTexture = skyboxCubeTexture;
            this.skyboxTexture = skyboxCubeTexture.clone();
            if (!envJson.show_background || envJson.is_editor) {
                let skyboxMesh = BABYLON.Mesh.CreateBox('skybox', 50.0, scene);
                let skyboxMaterial = <BABYLON.PBRMaterial>scene.getMaterialByName('skyBoxMat') || new BABYLON.PBRMaterial('skyBoxMat', scene);
                skyboxMaterial.backFaceCulling = false;
                skyboxMaterial.reflectionTexture = this.skyboxTexture;
                skyboxMaterial.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
                skyboxMaterial.microSurface = 1;
                skyboxMaterial.sideOrientation = 0;
                skyboxMesh.material = skyboxMaterial;
                skyboxMesh.infiniteDistance = false;
                skyboxMesh.isPickable = false;
                // hdrSkybox.freezeWorldMatrix();
            }
        }

        private createMirror(envJson: IEnvironmentJson, meshes: BABYLON.AbstractMesh[], scene: BABYLON.Scene) {
            if (envJson.show_reflective || envJson.is_editor) {
                let refl = (<BABYLON.StandardMaterial>scene.getMeshByName('reflectionPlane').material).reflectionTexture;
                for (let i = 0; i < meshes.length; i++) {
                    if (meshes[i].name !== 'reflectionPlane' && meshes[i].name !== 'groundPlane') {
                        (<BABYLON.MirrorTexture>refl).renderList.push(meshes[i]);
                    }
                }
                if (!envJson.show_background || envJson.is_editor) {
                    (<BABYLON.MirrorTexture>refl).renderList.push(scene.getMeshByName('skybox'));
                }
            }
        }

        setReflection(scene: BABYLON.Scene) {
            for (let i = 0; i < scene.materials.length; i++) {
                let mat = <BABYLON.PBRMaterial>scene.materials[i];
                if (mat.name.indexOf('Component_') > -1) {
                    mat.reflectionTexture = this.reflectionTexture;
                    mat.refractionTexture = mat.refractionTexture ? this.reflectionTexture : null;
                }
            }
        }
    }
}