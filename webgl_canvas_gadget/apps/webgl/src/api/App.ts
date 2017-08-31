namespace CG {
    export interface IParams extends IEnvironmentJson {
        materials: IMaterialJson[];
    }
    export class App {
        static Instance: App;
        scene: BABYLON.Scene;
        environment: Environment;
        uploadManager: UploadManager;
        materialManager: MaterialManager;
        lensFlareSystem: LensFlareSystem;
        animationManager: AnimationManager;
        cardManager: CardManager;
        modelMeshes: BABYLON.AbstractMesh[] = [];
        canvas: HTMLCanvasElement;

        private renderRequested: boolean = true;
        rotateCamera: boolean = false;
        shouldRotateCamera: boolean = false;
        rotationSpeed: number = 0;
        isEditor: boolean = false;

        constructor(canvas: HTMLCanvasElement, params: Project, sceneReady: () => void) {
            if (App.Instance == null) {
                App.Instance = this;
            }
            else {
                return App.Instance;
            }
            
            this.canvas = canvas;
            this.isEditor = false;

            Tools.logMessage('Application started');
            
            let engine = new BABYLON.Engine(this.canvas, true);
            engine.enableOfflineSupport = false;

            this.scene = this.createScene(params, engine);

            // Due to blender export problems, fix few things
            this.scene.executeWhenReady(() => {
                this.uploadManager.cleanTexturesArray();
                this.uploadManager.applyBumpTextures();
                this.scene.freezeMaterials();

                // Eliminate articats with transparent textures/ meshes
                for (let i = 0; i < this.scene.materials.length; i++) {
                    this.scene.materials[i].markDirty();
                }

                for (let i = 0; i < this.scene.meshes.length; i++) {
                    if (this.scene.meshes[i].name !== 'background') {
                        this.scene.meshes[i].freezeWorldMatrix();
                    }
                }

                this.renderRequested = true;
                this.registerRotateCamera(this.scene);
                Tools.logMessage('Application is ready');
                
                sceneReady();
                this.scene.render();
            });

            engine.runRenderLoop(() => {
                if (!this.renderRequested && ((<BABYLON.ArcRotateCamera>this.scene.activeCamera).inertialAlphaOffset !== 0
                    || (<BABYLON.ArcRotateCamera>this.scene.activeCamera).inertialBetaOffset !== 0
                    || (<BABYLON.ArcRotateCamera>this.scene.activeCamera).inertialRadiusOffset !== 0
                    || this.scene._activeAnimatables.length > 0)) {
                    this.renderRequested = true;
                    
                    //trigger mousedown event on rotation of camera for canvas element
                    
                    let d = document.createEvent("MouseEvents");
                    d.initMouseEvent("mousedown",true,true,window,0,0,0,0,0,false,false,false,false,0,null);
                    
                    this.canvas.dispatchEvent(d);
                }

                if (!this.renderRequested && this.rotateCamera) {
                    this.autoRotateCamera();
                    this.renderRequested = true;
                }

                if (this.isEditor || this.renderRequested || this.scene.activeCamera.name === 'VR') {
                    this.scene.render();
                    this.renderRequested = false;
                }
            });

            window.addEventListener('resize', () => {
                engine.resize();
                this.renderRequested = true;
            });
        }

        createScene(params: Project, engine: BABYLON.Engine): BABYLON.Scene {
            let scene = new BABYLON.Scene(engine);
            scene.clearColor = BABYLON.Color3.White();
            scene.autoClear = false;

            this.disableUnusedObjects(params, scene);

            this.environment = new Environment(params.environment, scene);
            this.lensFlareSystem = new LensFlareSystem(scene);
            this.materialManager = new MaterialManager(params.material_set, scene);
            this.uploadManager = new UploadManager(scene, this.environment);
            this.cardManager = new CardManager(scene);
            this.animationManager = new AnimationManager(scene);

            return scene;
        }

        private disableUnusedObjects(params: Project, scene: BABYLON.Scene): void {
            if (!this.isEditor) {
                scene.shadowsEnabled = false;
                scene.collisionsEnabled = false;
                scene.fogEnabled = false;
                scene.particlesEnabled = false;
                scene.postProcessesEnabled = false;
                scene.probesEnabled = false;
                scene.proceduralTexturesEnabled = false;
                scene.audioEnabled = false;
                // BABYLON.SceneOptimizer.OptimizeAsync(scene, BABYLON.SceneOptimizerOptions.HighDegradationAllowed(14));
            }
        }

        private registerRotateCamera(scene: BABYLON.Scene): void {
//            if (this.shouldRotateCamera) {
//                $('body').inactivityTime({
//                    'timeout': 10000,
//                    'inactivityCallback': () => {
//                        this.rotateCamera = true;
//                        this.rotationSpeed = 0;
//                    },
//                    'activityCallback': () => {
//                        this.rotateCamera = false;
//                    },
//                });
//            }
        }

        private autoRotateCamera() {
            this.rotationSpeed = this.rotationSpeed + 0.00166666666 > 0.25 ? 0.25 : this.rotationSpeed + 0.00166666666;
            (<BABYLON.ArcRotateCamera>this.scene.activeCamera).alpha += this.rotationSpeed / 60;
        }

        requestRender() {
            this.renderRequested = true;
        }
    }
}