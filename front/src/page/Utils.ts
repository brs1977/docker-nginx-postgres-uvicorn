export class FailError extends Error {
    constructor(message:string) {
        super(message)
    }

}

export function fail(message='') {
    throw new FailError(message)
}

export async function sleep(tm:number) {
    return new Promise(resolve => {
        setTimeout(resolve,tm)
    })
}

export function createElement<T extends HTMLElement>(html:string) {
    const r = document.createRange()
    const f = r.createContextualFragment(html)
    return f.querySelector<T>('*:first-child')!
}

export function createFragment(html:string) {
    const r = document.createRange()
    return r.createContextualFragment(html)
}


