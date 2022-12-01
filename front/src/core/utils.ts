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