namespace CG {
    export interface IMaterialJson {
        id: number;
        name: string;
        thumbnail: string;
        compNum: number;
        subCompNum: number;
        isGlass: boolean;
        alpha: number;
        indexOfRefraction: number;
        directIntensity: number;
        emissiveIntensity: number;
        environmentIntensity: number;
        specularIntensity: number;
        overloadedShadowIntensity: number;
        overloadedShadeIntensity: number;
        cameraExposure: number;
        cameraContrast: number;
        microSurface: number;
        reflectivityColor: BABYLON.Color3;
        normal_map: string;
    }

    export class Material implements IMaterialJson {
        id: number;
        name: string;
        thumbnail: string;
        compNum: number;
        subCompNum: number;
        isGlass: boolean;
        alpha: number;
        indexOfRefraction: number;
        directIntensity: number;
        emissiveIntensity: number;
        environmentIntensity: number;
        specularIntensity: number;
        overloadedShadowIntensity: number;
        overloadedShadeIntensity: number;
        cameraExposure: number;
        cameraContrast: number;
        microSurface: number;
        reflectivityColor: BABYLON.Color3;
        normal_map: string;

        constructor(material: IMaterialJson, scene: BABYLON.Scene) {
            this.id = material.id;
            this.thumbnail = material.thumbnail;
            this.name = material.name;
            this.isGlass = JSON.parse(<any>material.isGlass);
            this.indexOfRefraction = material.indexOfRefraction;
            this.alpha = material.alpha;
            this.directIntensity = material.directIntensity;
            this.emissiveIntensity = material.emissiveIntensity;
            this.environmentIntensity = material.environmentIntensity;
            this.specularIntensity = material.specularIntensity;
            this.overloadedShadowIntensity = material.overloadedShadowIntensity;
            this.overloadedShadeIntensity = material.overloadedShadeIntensity;
            this.cameraExposure = material.cameraExposure;
            this.cameraContrast = material.cameraContrast;
            this.microSurface = material.microSurface;
            this.normal_map = material.normal_map;
            this.reflectivityColor = new BABYLON.Color3(material.reflectivityColor.r, material.reflectivityColor.g, material.reflectivityColor.b);
        }

        public ToJSON(): string {
            return '{' +
                '"name":"' + this.name + '",' +
                '"isGlass":"' + this.isGlass + '",' +
                '"indexOfRefraction":' + this.indexOfRefraction.toPrecision(2) + ',' +
                '"alpha":' + this.alpha.toPrecision(2) + ',' +
                '"directIntensity":' + this.directIntensity.toPrecision(2) + ',' +
                '"emissiveIntensity":' + this.emissiveIntensity.toPrecision(2) + ',' +
                '"environmentIntensity":' + this.environmentIntensity.toPrecision(2) + ',' +
                '"specularIntensity":' + this.specularIntensity.toPrecision(2) + ',' +
                '"overloadedShadowIntensity":' + this.overloadedShadowIntensity.toPrecision(2) + ',' +
                '"overloadedShadeIntensity":' + this.overloadedShadeIntensity.toPrecision(2) + ',' +
                '"cameraExposure":' + this.cameraExposure.toPrecision(2) + ',' +
                '"cameraContrast":' + this.cameraContrast.toPrecision(2) + ',' +
                '"microSurface":' + this.microSurface.toPrecision(2) + ',' +
                '"reflectivityColor":{"r":' + this.reflectivityColor.r.toPrecision(2) + ', "g":' + this.reflectivityColor.g.toPrecision(2) + ', "b":' + this.reflectivityColor.b.toPrecision(2) + '}' +
                '}';
        }
    }
}