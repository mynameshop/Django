namespace CG {
    export class EnvironmentEditor {
        constructor(private scene: BABYLON.Scene, private environment: Environment) {
            $('body').on('editorPropertyChanged', (e: any) => {
                switch (e.name) {
                    case 'show_background': this.turnBackgroundOnOff(e.value); break;
                    case 'show_ground_plane': this.turnGroundPlaneOffOn(e.value); break;
                    case 'show_shadow': this.turnShadowOffOn(e.value); break;
                    case 'show_reflective': this.turnReflectivePlaneOffOn(e.value); break;
                    case 'gradient_top_hue': this.changeTopGradientHue(e.value); break;
                    case 'gradient_top_lightness': this.changeTopGradientLightness(e.value); break;
                    case 'gradient_bottom_hue': this.changeBottomGradientHue(e.value); break;
                    case 'gradient_bottom_lightness': this.changeBottomGradientLightness(e.value); break;
                    case 'gradient_offset': this.changeGradientOffset(e.value); break;
                    case 'reflective_amount': this.changeReflectionAmount(e.value); break;
                    case 'ground_plane_scale': this.changeGroundPlaneSize(e.value); break;
                    case 'skybox': this.setSkybox(e.value.url, e.value.id); break;
                    case 'ground_plane': this.updateGroundTexture(e.value.url); break;
                }
                App.Instance.requestRender();
            });
        }

        turnBackgroundOnOff(value: boolean): void {
            this.environment.backgroundMesh.setEnabled(value);
        }

        turnShadowOffOn(value: boolean): void {
            this.environment.groundShadowEnabled = value;
            if (this.environment.groundShadow) {
                this.environment.groundShadow.setEnabled(value);
            }
        }

        setSkybox(skyboxUrl: string, id: number): void {
            this.environment.reflectionTexture.dispose();
            this.environment.reflectionTexture = null;

            this.environment.skyboxTexture.dispose();
            this.environment.skyboxTexture = null;

            let hdr = new BABYLON.CubeTexture(skyboxUrl + 'skybox', this.scene);
            this.environment.reflectionTexture = hdr.clone();
            this.environment.skyboxTexture = hdr.clone();

            let skyMat = <BABYLON.PBRMaterial>this.scene.getMaterialByName('skyBoxMat');
            if (!skyMat) {
                skyMat = new BABYLON.PBRMaterial('skyBoxMat', this.scene);
            }

            skyMat.reflectionTexture = this.environment.skyboxTexture;
            skyMat.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;

            (<BABYLON.Mesh>this.scene.getMeshByName('skybox')).material = skyMat;

            this.environment.setReflection(this.scene);
        }

        changeTopGradientHue(value: string): void {
            this.environment.hueT = parseFloat(value);
            let ints = Tools.hslToRgb(this.environment.hueT, this.environment.saturationT, this.environment.ligthnessT);
            (<BABYLON.ShaderMaterial>this.environment.backgroundMesh.material).setColor3('topColor', BABYLON.Color3.FromInts(ints[0], ints[1], ints[2]));
        }

        changeTopGradientLightness(value: string): void {
            this.environment.ligthnessT = parseFloat(value);
            let ints = Tools.hslToRgb(this.environment.hueT, this.environment.saturationT, this.environment.ligthnessT);
            (<BABYLON.ShaderMaterial>this.environment.backgroundMesh.material).setColor3('topColor', BABYLON.Color3.FromInts(ints[0], ints[1], ints[2]));
        }

        changeBottomGradientHue(value: string): void {
            this.environment.hueB = parseFloat(value);
            let ints = Tools.hslToRgb(this.environment.hueB, this.environment.saturationB, this.environment.ligthnessB);
            (<BABYLON.ShaderMaterial>this.environment.backgroundMesh.material).setColor3('bottomColor', BABYLON.Color3.FromInts(ints[0], ints[1], ints[2]));
        }

        changeBottomGradientLightness(value: string): void {
            this.environment.ligthnessB = parseFloat(value);
            if (this.environment.ligthnessB < 0) { this.environment.ligthnessB = 0; }
            let ints = Tools.hslToRgb(this.environment.hueB, this.environment.saturationB, this.environment.ligthnessB);
            (<BABYLON.ShaderMaterial>this.environment.backgroundMesh.material).setColor3('bottomColor', BABYLON.Color3.FromInts(ints[0], ints[1], ints[2]));
        }

        changeGradientOffset(value: number): void {
            this.environment.gradientOffset = value;
            (<BABYLON.ShaderMaterial>this.environment.backgroundMesh.material).setFloat('offset', value);
        }

        updateGroundTexture(url: string): void {
            let mesh = this.scene.getMeshByName('groundPlane');
            if ((<BABYLON.PBRMaterial>mesh.material).albedoTexture) {
                (<BABYLON.PBRMaterial>mesh.material).albedoTexture.dispose();
            }
            if ((<BABYLON.PBRMaterial>mesh.material).opacityTexture) {
                (<BABYLON.PBRMaterial>mesh.material).opacityTexture.dispose();
            }
            this.environment.groundTexture = new BABYLON.Texture(url, this.scene);
            (<BABYLON.PBRMaterial>mesh.material).albedoTexture = this.environment.groundTexture;
            (<BABYLON.PBRMaterial>mesh.material).opacityTexture = this.environment.groundTexture;
            (<BABYLON.PBRMaterial>mesh.material).albedoTexture.hasAlpha = true;
        }

        turnGroundPlaneOffOn(value: boolean): void {
            this.environment.groundMesh.setEnabled(value);
        }

        changeGroundPlaneSize(scale: number): void {
            this.environment.groundMesh.scaling = new BABYLON.Vector3(scale, scale, scale);
        }

        turnReflectivePlaneOffOn(value: boolean): void {
            this.environment.reflectiveMesh.setEnabled(value);
        }

        changeReflectionAmount(value: number): void {
            this.environment.reflectiveMesh.material.alpha = value;
        }
    }
}