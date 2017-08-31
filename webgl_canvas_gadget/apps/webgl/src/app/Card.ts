namespace CG {
    export class Card {
        modelId: number;
        anchorId: number;
        lineId: number;
        id: number;

        card: BABYLON.Mesh;
        tiltedLine: BABYLON.Mesh;
        screenPosition: BABYLON.Vector3;
        anchor: BABYLON.Mesh;
        horizontalLine: BABYLON.Mesh;
        left: boolean;
        right: boolean;
        box: BABYLON.Mesh;
        screenPositionAnchor: BABYLON.Vector3;

        gettingSmaller: boolean;
        gettingBigger: boolean;
        minimazed: boolean;
        maximazed: boolean;
        notResizing: boolean;
        scalingFactor: number;

        titleFontSize: string;
        cardHeight: number;
        fontTextureHeight: number;
        descriptionTextStartPosition: number;
        titleTextStart: number;
        ctx;

        constructor(json: any, scene: BABYLON.Scene, pos?: BABYLON.Vector3) {
            if (json.callout_style.image.indexOf('collapsed') > -1) {
                this.cardHeight = 0.13;
                this.titleFontSize = '100px';
                this.fontTextureHeight = 128;
                this.descriptionTextStartPosition = 260;
                this.titleTextStart = 100;
            }
            else if (json.callout_style.image.indexOf('3') > -1) {
                this.cardHeight = 0.48;
                this.titleFontSize = '115px';
                this.fontTextureHeight = 500;
                this.descriptionTextStartPosition = 315;
                this.titleTextStart = 115;
            }
            else {
                this.cardHeight = 0.48;
                this.titleFontSize = '115px';
                this.fontTextureHeight = 500;
                this.descriptionTextStartPosition = 260;
                this.titleTextStart = 115;
            }

            this.gettingSmaller = false;
            this.gettingBigger = false;
            this.notResizing = true;
            this.maximazed = true;
            this.minimazed = false;
            this.scalingFactor = 0.05;

            this.id = json.id;
            this.modelId = json.model3d;

            this.left = false;
            this.right = false;

            this.lineId = json.line_style.id;
            this.anchorId = json.anchor_style.id;

            ////////// Box for resize 

            this.box = BABYLON.MeshBuilder.CreateBox('box', { size: 0.1 }, scene);

            if (pos) {
                this.box.position.x = pos.x;
                this.box.position.y = pos.y;
                this.box.position.z = pos.z;
            }
            else {
                this.box.position = new BABYLON.Vector3(json.pos.x, json.pos.y, json.pos.z);
            }

            this.box.isVisible = false;
            this.box.isPickable = false;
            this.box.scaling = new BABYLON.Vector3(0.6, 0.6, 0.6);

            //////////

            ////////// Card

            let texture = new BABYLON.DynamicTexture('texture', { width: 1200, height: this.fontTextureHeight }, scene, true);
            texture.hasAlpha = true;

            let textureBackground = new BABYLON.Texture(json.callout_style.image, scene);
            textureBackground.hasAlpha = true;

            this.ctx = texture.getContext();
            this.ctx.imageSmoothingEnabled = true;
            this.ctx.mozImageSmoothingEnabled = true;
            this.ctx.msImageSmoothingEnabled = true;
            this.ctx.oImageSmoothingEnabled = true;

            let shaderMaterial = new BABYLON.ShaderMaterial('cardhader', scene,
                {
                    vertexElement: 'cardVertexShader',
                    fragmentElement: 'cardFragmentShader',
                },
                {
                    needAlphaBlending: true,
                    attributes: ['position', 'uv'],
                    uniforms: ['worldViewProjection'],
                    samplers: ['backgroundImage', 'textImage']
                });

            textureBackground.wrapU = BABYLON.Texture.CLAMP_ADDRESSMODE;
            textureBackground.wrapV = BABYLON.Texture.CLAMP_ADDRESSMODE;

            shaderMaterial.setTexture('backgroundImage', textureBackground);
            shaderMaterial.setTexture('textImage', texture);

            texture.update();

            this.card = BABYLON.MeshBuilder.CreatePlane('planeBackground', { width: 1.5, height: this.cardHeight }, scene);
            this.card.material = shaderMaterial;
            this.card.renderingGroupId = 3;
            this.card.isPickable = false;
            this.card.setPivotMatrix(BABYLON.Matrix.Translation(-2, 0.75, 0));
            this.card.parent = this.box;
            //////////

            ////////// Horizontal Line

            this.horizontalLine = BABYLON.MeshBuilder.CreatePlane('horizontalLine', { width: 0.5, height: 0.5 }, scene);

            this.horizontalLine.parent = this.card;
            this.horizontalLine.rotate(new BABYLON.Vector3(0, 0, 1), Math.PI / 2, BABYLON.Space.LOCAL);

            this.horizontalLine.position.x = 1;
            this.horizontalLine.renderingGroupId = 2;
            this.horizontalLine.isPickable = false;

            let lineBackground = new BABYLON.Texture(json.line_style.image, scene);
            lineBackground.hasAlpha = true;

            let planeHorizontalLineMaterial = new BABYLON.StandardMaterial('horizontalLine', scene);
            planeHorizontalLineMaterial.diffuseTexture = lineBackground;
            planeHorizontalLineMaterial.ambientColor = new BABYLON.Color3(1, 1, 1);
            planeHorizontalLineMaterial.emissiveColor = BABYLON.Color3.White();

            this.horizontalLine.material = planeHorizontalLineMaterial;

            //////////
            ////////// Tilted line 

            this.tiltedLine = BABYLON.MeshBuilder.CreatePlane('tiltedLineTop', { width: 0.5, height: 1 }, scene);
            this.tiltedLine.renderingGroupId = 2;
            this.tiltedLine.isPickable = false;
            this.tiltedLine.parent = this.card;

            this.tiltedLine.translate(new BABYLON.Vector3(1, 0, 0), 1.6, BABYLON.Space.LOCAL);
            this.tiltedLine.translate(new BABYLON.Vector3(0, 1, 0), -0.355, BABYLON.Space.LOCAL);
            this.tiltedLine.translate(new BABYLON.Vector3(0, 0, 1), 0, BABYLON.Space.LOCAL);
            // this.tiltedLine.rotate(new BABYLON.Vector3(0, 0, 1), Math.PI / 4, BABYLON.Space.LOCAL);

            let tiltedLineBackground = new BABYLON.Texture(json.line_style.image, scene);
            tiltedLineBackground.hasAlpha = true;

            let planeTiltedLineMaterial = new BABYLON.StandardMaterial('tiltedLine', scene);
            planeTiltedLineMaterial.diffuseTexture = tiltedLineBackground;
            (<BABYLON.Texture>planeTiltedLineMaterial.diffuseTexture).vScale = 2;

            planeTiltedLineMaterial.specularColor = BABYLON.Color3.Black();
            planeTiltedLineMaterial.emissiveColor = BABYLON.Color3.White();
            planeTiltedLineMaterial.backFaceCulling = false;

            this.tiltedLine.material = planeTiltedLineMaterial;

            //////////

            ////////// Anchror mesh

            this.anchor = BABYLON.MeshBuilder.CreatePlane('anchor', { width: 0.15, height: 0.15 }, scene);

            this.anchor.position = this.box.position;
            this.anchor.scaling = new BABYLON.Vector3(0.6, 0.6, 0.6);
            this.anchor.isPickable = false;
            this.anchor.renderingGroupId = 1;

            let anchorBackground = new BABYLON.Texture(json.anchor_style.image, scene);
            anchorBackground.hasAlpha = true;

            let anchorMaterial = new BABYLON.StandardMaterial('anchorMaterial', scene);
            anchorMaterial.diffuseTexture = anchorBackground;
            anchorMaterial.emissiveColor = BABYLON.Color3.White();

            this.anchor.material = anchorMaterial;

            ////////// Set Card Text

            this.setTitle(json.label, texture);
            this.setDescription(json.text, texture);

            //////////
        }

        update(scene: BABYLON.Scene): void {

            if (this.gettingBigger === true && this.notResizing === false) {
                this.box.scaling.x += this.scalingFactor;
                this.box.scaling.y += this.scalingFactor;
                this.box.scaling.z += this.scalingFactor;

                // this.tiltedLine.isVisible = true;

                if (this.box.scaling.x >= 0.6) {
                    this.box.scaling = new BABYLON.Vector3(0.6, 0.6, 0.6);
                    this.maximazed = true;
                    this.gettingBigger = false;
                    this.gettingSmaller = false;
                    this.minimazed = false;
                    this.notResizing = true;
                    this.scalingFactor = 0.035;
                }
            }

            if (this.gettingSmaller === true && this.notResizing === false) {
                this.box.scaling.x -= this.scalingFactor;
                this.box.scaling.y -= this.scalingFactor;
                this.box.scaling.z -= this.scalingFactor;

                // this.tiltedLine.isVisible = false;

                if (this.box.scaling.x <= 0) {
                    this.box.scaling = BABYLON.Vector3.Zero();
                    this.maximazed = false;
                    this.gettingBigger = false;
                    this.gettingSmaller = false;
                    this.notResizing = true;
                    this.minimazed = true;
                    this.scalingFactor = 0.035;
                }
            }

            this.anchor.rotation.y = -(<BABYLON.ArcRotateCamera>scene.activeCamera).alpha - (Math.PI / 2);
            this.anchor.rotation.x = -(<BABYLON.ArcRotateCamera>scene.activeCamera).beta + (Math.PI / 2);

            this.screenPositionAnchor = BABYLON.Vector3.Project(this.anchor.getAbsolutePosition(), BABYLON.Matrix.Identity(), scene.getTransformMatrix(), scene.activeCamera.viewport.toGlobal(scene.getEngine().getRenderWidth(), scene.getEngine().getRenderHeight()));

            let canvasWidth = scene.getEngine().getRenderWidth();

            if (this.left === false && this.right === false) {
                if (canvasWidth / 2 > this.screenPositionAnchor.x && this.screenPositionAnchor !== null) {
                    // line on right side of card

                    this.right = true;
                    this.left = false;
                    this.tiltedLine.rotate(new BABYLON.Vector3(0, 0, 1), Math.PI / 4, BABYLON.Space.LOCAL);
                }
                if (canvasWidth / 2 < this.screenPositionAnchor.x && this.screenPositionAnchor !== null) {
                    // line on left side of card 

                    this.left = true;
                    this.right = false;

                    this.horizontalLine.position.x = -0.997;

                    this.tiltedLine.position.x = -1.6;
                    this.tiltedLine.rotate(new BABYLON.Vector3(0, 0, 1), -Math.PI / 4, BABYLON.Space.LOCAL);

                    this.card.setPivotMatrix(BABYLON.Matrix.Translation(2, 0.75, 0));

                }
            }

            if (canvasWidth / 2 > this.screenPositionAnchor.x && this.left === true && this.screenPositionAnchor !== null) {
                // line on right side of card

                this.horizontalLine.position.x = 0.997;
                this.tiltedLine.position.x = 1.6;
                this.tiltedLine.rotate(new BABYLON.Vector3(0, 0, 1), Math.PI / 2, BABYLON.Space.LOCAL);

                this.card.setPivotMatrix(BABYLON.Matrix.Translation(-2, 0.75, 0));

                this.left = false;
                this.right = true;

            }

            if (canvasWidth / 2 < this.screenPositionAnchor.x && this.right === true && this.screenPositionAnchor !== null) {
                // line on left side of card 

                this.horizontalLine.position.x = -0.997;
                this.tiltedLine.position.x = -1.6;
                this.tiltedLine.rotate(new BABYLON.Vector3(0, 0, 1), -Math.PI / 2, BABYLON.Space.LOCAL);

                this.card.setPivotMatrix(BABYLON.Matrix.Translation(2, 0.75, 0));

                this.left = true;
                this.right = false;

            }

            this.card.rotation.y = -(<BABYLON.ArcRotateCamera>scene.activeCamera).alpha - (Math.PI / 2);
            this.card.rotation.x = -(<BABYLON.ArcRotateCamera>scene.activeCamera).beta + (Math.PI / 2);

            let direction = this.anchor.position.subtract(scene.activeCamera.position);

            let distance = BABYLON.Vector3.Distance(scene.activeCamera.position, this.anchor.position);
            direction.normalize();

            let ray = new BABYLON.Ray(scene.activeCamera.position, direction);
            let pickInfo = scene.pickWithRay(ray, null, false);
            if (pickInfo.distance < distance) {
                this.tiltedLine.isVisible = false;
                this.anchor.isVisible = false;
                this.card.isVisible = false;
                this.horizontalLine.isVisible = false;
            }
            else {
                if (this.maximazed) {
                    this.tiltedLine.isVisible = true;
                    this.card.isVisible = true;
                    this.horizontalLine.isVisible = true;
                }
                this.anchor.isVisible = true;
            }

        }

        setTitle(text: string, texture: BABYLON.DynamicTexture) {
            if (text.indexOf('j') > -1 || text.indexOf('q') > -1 || text.indexOf('p') > -1 || text.indexOf('y') > -1 || text.indexOf('g') > -1) {
                this.titleTextStart -= 20;
            }
            else {
                this.titleTextStart -= 0;
            }
            this.ctx.fillStyle = '#ffffff';
            this.ctx.font = 'bold ' + this.titleFontSize + ' Quattrocento Sans';

            // 40 107

            this.ctx.fillText(text, 40, this.titleTextStart);

            texture.update();
        }

        setDescription(text: string, texture: BABYLON.DynamicTexture) {
            this.ctx.fillStyle = '#ffffff';
            this.ctx.font = '120px Quattrocento Sans';

            this.wrapText(text, 40, this.descriptionTextStartPosition, 2000, 130);
            texture.update();
        }

        wrapText(text, x, y, maxWidth, lineHeight) {
            let words = text.split(' ');
            let line = '';

            for (let n = 0; n < words.length; n++) {
                let testLine = line + words[n] + ' ';
                let metrics = this.ctx.measureText(testLine);
                let testWidth = metrics.width;
                if (testWidth > maxWidth && n > 0) {
                    this.ctx.fillText(line, x, y);
                    line = words[n] + ' ';
                    y += lineHeight;
                }
                else {
                    line = testLine;
                }
            }

            this.ctx.fillText(line, x, y);
        }

        dispose() {
            // this.texture.dispose();
            // this.texture = null;
            // this.textureBackground.dispose();
            // this.textureBackground = null;
            this.ctx = null;

            this.card.material.dispose(true, true);
            this.card.dispose();
            this.card = null;

            this.tiltedLine.material.dispose(true, true);
            this.tiltedLine.dispose();
            this.tiltedLine = null;

            this.anchor.material.dispose(true, true);
            this.anchor.dispose();
            this.anchor = null;

            this.horizontalLine.material.dispose(true, true);
            this.horizontalLine.dispose();
            this.horizontalLine = null;

            this.box.dispose();
            this.box = null;
        }
    }
}