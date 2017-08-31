namespace CG {
	
	export interface IModel2D {
        id: number;
    }
	
	export class Model2D implements IModel2D{
		id: number;
		
		constructor(data: IModel2D) {
			this.id = data.id;
		}
	}
	
}