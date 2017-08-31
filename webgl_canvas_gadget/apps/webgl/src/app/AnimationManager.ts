namespace CG {
    export interface IAnimationMetaJson {
        type: string;
        animations: IAnimationJson[];
    }

    export class AnimationManager {
        type: string;
        animations: Animation[] = [];
        currentAnimation: number = 0;
        isAnimating: boolean = false;

        constructor(private scene: BABYLON.Scene) {
        }

        loadFromJson(json: IAnimationMetaJson): void {
            for (let i = 0; i < this.animations.length; i++) {
                this.animations[i].dispose();
            }
            this.animations.splice(0, this.animations.length);
            this.currentAnimation = 0;
        	this.isAnimating = false;

            if (json) {
                this.type = json.type;
                if (json.animations) {
                    for (let i = 0; i < json.animations.length; i++) {
                        let anim = new Animation(json.animations[i], this.scene);
                        if (anim.target == null) {
                            continue;
                        }
                        this.animations.push(anim);
                    }
                }
                Tools.logMessage('animations done');
            }
        }

        animate(index: number): void {
            switch (this.type) {
                case 'individual':
                    this.playAnimationIndividual(index);
                    break;
                case 'cascade':
                    this.playAnimationCascade(index);
                    break;
                default:
                    break;
            }
        }

        playAnimationIndividual(index: number): void {
            if (this.isAnimating) {
                return;
            }
            
            if (index !== this.currentAnimation && this.animations[this.currentAnimation].nextState === NextAnimationState.Reverse) {
                if (!this.animations[index].auto_reverse) {
                	this.currentAnimation = index
                	
                	this.animations[this.currentAnimation].onAnimationEnd = () => {
	                    this.isAnimating = false;
                        this.currentAnimation = index;
	                };
                }else {
                	this.animations[this.currentAnimation].onAnimationEnd = () => {
	                    this.animations[index].onAnimationEnd = () => {
	                        this.isAnimating = false;
	                        this.currentAnimation = index;
	                    };
	                    this.animations[index].animateNextState();
	                };
                }
                
                this.isAnimating = true;
                this.animations[this.currentAnimation].animateNextState();
            }
            else {
                this.animations[index].onAnimationEnd = () => {
                    this.isAnimating = false;
                    this.currentAnimation = index;
                };
                this.isAnimating = true;
                this.animations[index].animateNextState();
            }
        }

        playAnimationCascade(index: number): void {
            if (this.isAnimating) {
                return;
            }
            this.isAnimating = true;
            if (index === this.currentAnimation) {
                this.animations[index].onAnimationEnd = () => {
                    this.isAnimating = false;
                    return;
                };
                if(this.animations[index]) {
                	this.animations[index].animateNextState();
                }
            }
            else if (index > this.currentAnimation) {
                for (let i = this.currentAnimation; i <= index; i++) {
                    this.animations[i].onAnimationEnd = () => {
                        if (i === index || i === this.animations.length - 1) {
                            this.isAnimating = false;
                            this.currentAnimation = index;
                            return;
                        }
                        if(this.animations[i + 1]) {
                        	this.animations[i + 1].animateNextState(NextAnimationState.Forward);
                        }
                    };
                }
                if (!this.animations[this.currentAnimation].animateNextState(NextAnimationState.Forward)) {
                    this.animations[this.currentAnimation + 1].animateNextState(NextAnimationState.Forward);
                }
                return;
            }
            else {
                for (let i = this.currentAnimation; i >= index; i--) {
                    this.animations[i].onAnimationEnd = () => {
                        if (i === index || i === 0) {
                            this.isAnimating = false;
                            this.currentAnimation = index;
                            return;
                        }
                        if(this.animations[i - 1]) {
                        	this.animations[i - 1].animateNextState(NextAnimationState.Reverse);
                        }
                    };
                }

                if (!this.animations[this.currentAnimation].animateNextState(NextAnimationState.Reverse)) {
                    this.animations[this.currentAnimation - 1].animateNextState(NextAnimationState.Reverse);
                }
                return;
            }
        }
    }
}