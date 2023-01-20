import { createElement } from "./Utils"

export class View<T extends HTMLElement> {
    
    readonly root: T
    
    constructor(html:string) {
        this.root = createElement<T>(html)
    }

}