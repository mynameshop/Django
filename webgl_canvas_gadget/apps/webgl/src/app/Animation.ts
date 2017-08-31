namespace CG {
    export interface IAnimation {
        startFrame: number;
        endFrame: number;
        events: IAnimationEvent[];
    }

    export interface IAnimationEvent {
        type: string;
        atFrame: number;
        component: string;
        subCompNum: number;
        texture: string;
        skipTo: number;
        from: number;
        to: number;
        target: string;
        material: any;
    	visibility: boolean;
    }

    export interface IAnimationJson {
        target: string;
        name: string;
        forward: IAnimation;
        reverse: IAnimation;
    	auto_reverse: boolean;
    }

    export enum NextAnimationState {
        Forward,
        Reverse
    }

    // needs major refactoring!!!!
    export class Animation {
        nextState: NextAnimationState;
        forwardStart: number;
        forwardEnd: number;
        reverseStart: number = -1;
        reverseEnd: number = -1;
        target: BABYLON.Skeleton;
        forwardEvents: BABYLON.AnimationEvent[] = [];
        reverseEvents: BABYLON.AnimationEvent[] = [];
    	auto_reverse: boolean;
        onAnimationEnd: any;
        currentAnimation: BABYLON.Animatable;
        loopingAnimation: BABYLON.Animatable = null;

        constructor(json: IAnimationJson, private scene: BABYLON.Scene) {
            this.target = scene.getSkeletonByName(json.target);
            if (this.target == null) {
                return;
            }
            this.auto_reverse = json.auto_reverse;
            this.nextState = NextAnimationState.Forward;

            // +1 due to blender shifting the animation timeline
            this.forwardStart = json.forward.startFrame + 1;
            this.forwardEnd = json.forward.endFrame + 1;
            if (json.reverse) {
                this.reverseStart = json.reverse.startFrame + 1;
                this.reverseEnd = json.reverse.endFrame + 1;
            }
            if (json.forward && json.forward.events) {
                for (let i = 0; i < json.forward.events.length; i++) {
                    json.forward.events[i].subCompNum = json.forward.events[i].subCompNum;// > -1 ? json.forward.events[i].subCompNum : -1;
                    this.forwardEvents.push(this.animationEvent(json.forward.events[i], scene));
                }
            }

            if (json.reverse && json.reverse.events) {
                for (let i = 0; i < json.reverse.events.length; i++) {
                    json.reverse.events[i].subCompNum = json.reverse.events[i].subCompNum;// > -1 ? json.reverse.events[i].subCompNum : -1;
                    this.reverseEvents.push(this.animationEvent(json.reverse.events[i], scene));
                }
            }
        }

        private cacheTexture(animEvent: IAnimationEvent) {
            if( animEvent.texture ){
                let cache = Tools.getTextureByUrl(animEvent.texture, this.scene) || new BABYLON.Texture(animEvent.texture, this.scene);
            }
        }

        private animationEvent(event: IAnimationEvent, scene: BABYLON.Scene): BABYLON.AnimationEvent {
            switch (event.type) {
                case 'textureSwap': {
                    this.fixEventTexture(event); 
                    this.cacheTexture(event);
                    return this.textureSwapAnimationEvent(event);
                }
                case 'setVisibility': {
                	return new BABYLON.AnimationEvent(event.atFrame + 1, () => {   
                    	const componentName = event.component;
                    	let subCompNum = event.subCompNum;
                    	let mesh = this.scene.getMeshByName(event.component);
                        let material = (<any>mesh.material);
                        if(material.subMaterials){
                            subCompNum = material.subMaterials.length - 1 - event.subCompNum;
                            material = material.subMaterials[ subCompNum ];
                        }
                    	
                    	const visibility = event.visibility;
                    	App.Instance.materialManager.setVisibility(visibility, componentName, subCompNum);
                    });
                }
                case 'skipFrames': return this.skipFramesAnimationEvent(event);
                case 'animation': return this.animationAnimationEvent(event);
                case 'loop': return this.loopAnimationEvent(event);
                default: console.warn('Unknown animation event type');
            }
        }

        private loopAnimationEvent(animEvent: IAnimationEvent): BABYLON.AnimationEvent {
            return new BABYLON.AnimationEvent(animEvent.atFrame + 1, () => {
                if (this.currentAnimation.onAnimationEnd && this.loopingAnimation == null) {
                    this.currentAnimation.onAnimationEnd();
                }
                this.currentAnimation.onAnimationEnd = () => {
                    this.loopingAnimation = this.scene.beginAnimation(this.scene.getSkeletonByName(animEvent.target), animEvent.from + 1, animEvent.to + 1, true, 1, null);
                };
                this.currentAnimation.stop();
            });
        }

        private animationAnimationEvent(animEvent: IAnimationEvent): BABYLON.AnimationEvent {
            return new BABYLON.AnimationEvent(animEvent.atFrame + 1, () => {
                this.scene.beginAnimation(this.scene.getSkeletonByName(animEvent.target), animEvent.from + 1, animEvent.to + 1);
            });
        }

        private skipFramesAnimationEvent(animEvent: IAnimationEvent): BABYLON.AnimationEvent {
            return new BABYLON.AnimationEvent(animEvent.atFrame + 1, () => {
                this.currentAnimation.fromFrame = animEvent.skipTo + 1;
            });
        }

        private fixEventTexture(animEvent: IAnimationEvent) {
            if( animEvent.texture ){
                let mesh = this.scene.getMeshByName(animEvent.component);
                let s = <string>animEvent.texture;
                let ss = s.split('/');
                
                let material = (<any>mesh.material);
                if(material.subMaterials){
                    material = material.subMaterials[ material.subMaterials.length - 1 - (animEvent.subCompNum || 0) ];
                }
                
                let sss = material.albedoTexture.getInternalTexture().url.split('/');
    
                sss.pop();
                s = sss.join('/') + '/' + ss[ss.length - 1];
                animEvent.texture = s;
            }
        }

        private textureSwapAnimationEvent(animEvent: IAnimationEvent): BABYLON.AnimationEvent {
            return new BABYLON.AnimationEvent(animEvent.atFrame + 1, () => {   
              let mesh = this.scene.getMeshByName(animEvent.component);
              let material = (<any>mesh.material);
              let subCompNum = animEvent.subCompNum;
              if(material.subMaterials){
                  subCompNum = material.subMaterials.length - 1 - animEvent.subCompNum;
                  material = material.subMaterials[ subCompNum ];
              }
              
              if( animEvent.texture ){
                  material.albedoTexture = Tools.getTextureByUrl(animEvent.texture, this.scene) || new BABYLON.Texture(animEvent.texture, this.scene);
                  material.opacityTexture = (animEvent.texture.indexOf('transparent') > -1) ? material.albedoTexture : null;
              }
              
              if( animEvent.material ) {
                  App.Instance.materialManager.ApplyMaterialToMesh(animEvent.material, animEvent.component, subCompNum);
              }
              material.markDirty();
              App.Instance.environment.setReflection(App.Instance.scene);
          });
        }

        animateNextState(animateOnly?: NextAnimationState): boolean {
            this.currentAnimation = null;

            if (animateOnly != null && animateOnly !== this.nextState) {
                return false;
            }

            if (this.reverseStart === -1 && this.reverseEnd === -1) {
                this.currentAnimation = this.scene.beginAnimation(this.target, this.forwardStart, this.forwardEnd, false, 1, this.onAnimationEnd);
                (<any>this.currentAnimation.getAnimations()[0])._events.splice(0, (<any>this.currentAnimation.getAnimations()[0])._events.length);

                for (let i = 0; i < this.forwardEvents.length; i++) {
                	if (this.forwardEvents[i]) {
	                    this.forwardEvents[i].isDone = false;
	                    this.currentAnimation.getAnimations()[0].addEvent(this.forwardEvents[i]);
                	}
                }
                return;
            }
            
            switch (this.nextState) {
                case NextAnimationState.Forward:
                    this.currentAnimation = this.scene.beginAnimation(this.target, this.forwardStart, this.forwardEnd, false, 1, this.onAnimationEnd);
                    // any = <BABYLON.Animation>
                    (<any>this.currentAnimation.getAnimations()[0])._events.splice(0, (<any>this.currentAnimation.getAnimations()[0])._events.length);

                    for (let i = 0; i < this.forwardEvents.length; i++) {
                    	if (this.forwardEvents[i]) {
	                        this.forwardEvents[i].isDone = false;
	                        this.currentAnimation.getAnimations()[0].addEvent(this.forwardEvents[i]);
                    	}
                    }
                    this.nextState = NextAnimationState.Reverse;
                    break;
                case NextAnimationState.Reverse:
                    if (this.loopingAnimation != null) {
                        this.currentAnimation = this.scene.beginAnimation(this.loopingAnimation.target, this.loopingAnimation.getAnimations()[0].currentFrame, this.loopingAnimation.toFrame, false, 1, this.onAnimationEnd);
                        this.loopingAnimation.stop();
                        this.loopingAnimation = null;

                        // any = <BABYLON.Animation> because _events is private
                        (<any>this.currentAnimation.getAnimations()[0])._events.splice(0, (<any>this.currentAnimation.getAnimations()[0])._events.length);

                        for (let i = 0; i < this.reverseEvents.length; i++) {
                        	if (this.reverseEvents[i]) {
	                            this.reverseEvents[i].isDone = false;
	                            this.currentAnimation.getAnimations()[0].addEvent(this.reverseEvents[i]);
                        	}
                        }
                        this.nextState = NextAnimationState.Forward;
                    }
                    else {
                        if (this.reverseEnd > 0) {
                            this.currentAnimation = this.scene.beginAnimation(this.target, this.reverseStart, this.reverseEnd, false, 1, this.onAnimationEnd);
                        }
                        else {
                            if (this.onAnimationEnd) {
                                this.onAnimationEnd();
                            }
                        }
                        // any = <BABYLON.Animation>
                        (<any>this.currentAnimation.getAnimations()[0])._events.splice(0, (<any>this.currentAnimation.getAnimations()[0])._events.length);

                        for (let i = 0; i < this.reverseEvents.length; i++) {
                            if (this.reverseEvents[i]) {
	                        	this.reverseEvents[i].isDone = false;
	                            this.currentAnimation.getAnimations()[0].addEvent(this.reverseEvents[i]);
                            }
                        }
                        this.nextState = NextAnimationState.Forward;
                        break;
                    }
            }
            return true;
        }

        dispose() {
            this.forwardEvents.splice(0, this.forwardEvents.length);
            this.forwardEvents = null;
            this.reverseEvents.splice(0, this.reverseEvents.length);
            this.reverseEvents = null;
            this.currentAnimation = null;
        }
    }
}