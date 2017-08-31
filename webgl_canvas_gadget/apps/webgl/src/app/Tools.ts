namespace CG {
    export class Tools {
        static hslToRgb(h: number, s: number, l: number) {
            let r, g, b;

            if (s === 0) {
                r = g = b = l; // achromatic
            } else {
                let hue2rgb = (p: number, q: number, t: number) => {
                    if (t < 0) { t += 1; }
                    if (t > 1) { t -= 1; }
                    if (t < 1 / 6) { return p + (q - p) * 6 * t; }
                    if (t < 1 / 2) { return q; }
                    if (t < 2 / 3) { return p + (q - p) * (2 / 3 - t) * 6; }
                    return p;
                };

                let q = l < 0.5 ? l * (1 + s) : l + s - l * s;
                let p = 2 * l - q;
                r = hue2rgb(p, q, h + 1 / 3);
                g = hue2rgb(p, q, h);
                b = hue2rgb(p, q, h - 1 / 3);
            }

            return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
        }

        static textureExists(url: string, scene: BABYLON.Scene): boolean {
            for (let i = 0; i < scene.textures.length; i++) {
                let _url = scene.textures[i].getInternalTexture().url;
                if (_url && _url === url) {
                    return true;
                }
            }
            return false;
        }

        static getTextureByUrl(url: string, scene: BABYLON.Scene): BABYLON.Texture {
            for (let i = 0; i < scene.textures.length; i++) {
                let _url = scene.textures[i].getInternalTexture().url;
                if (_url && _url === url) {
                    return <BABYLON.Texture>scene.textures[i];
                }
            }
            return null;
        }

        static logMessage(msg: string): void {
            if (App.Instance.isEditor) {
                console.log(msg);
            }
        }
    }
}