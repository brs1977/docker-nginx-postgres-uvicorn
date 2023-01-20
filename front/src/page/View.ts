import { createElement, createFragment } from "./Utils"

export class View<T extends HTMLElement> {
    
    readonly root: T
    
    constructor(html:string) {
        this.root = createElement<T>(html)
    }

}

export class Fragment {
    
    readonly root: DocumentFragment
    
    constructor(html:string) {
        this.root = createFragment(html)
    }

}