import { API } from "./PageTypes"
import { fail } from "./Utils"

export function getURL(pathname:string,port:number,serverURL?:string) {
    const url = new URL(serverURL ?? location.origin)
    url.pathname = pathname
    url.port = '' + port
    return url.toString()
}

export class ServerAPI implements API {
    
    token: string | undefined = undefined

    constructor(readonly url:string) {
    }

    async get<T>(action:string,params?:any):Promise<T> {
        const url = new URL(`${this.url}/${action}`)
        if (params)
            url.search = new URLSearchParams(params).toString()
        const options:RequestInit = {
            method: 'GET',
            //mode: 'same-origin',
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'include', // include, *same-origin, include
            headers: {
               'Content-Type': 'application/json',
            //    "Sec-Fetch-Dest": "empty",
            //    "Sec-Fetch-Mode": "no-cors",
            //    "Sec-Fetch-Site": "same-site"
              // 'Content-Type': 'application/x-www-form-urlencoded',
              ...(this.token ? {'Authorization': `Bearer ${this.token}`} : {})
            },            
        }
        // console.log(options)
        const res = await fetch(url,options)
        if (!res.ok) {
            fail(`${res.status} ${res.statusText}`)
        }
        const json = await res.json()
        return json
    }

    async post<T>(action:string,params:any):Promise<T> {
        const options:RequestInit = {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'include', // include, *same-origin, include
            headers: {
               'Content-Type': 'application/json',
              // 'Content-Type': 'application/x-www-form-urlencoded',
            },            
            body: JSON.stringify(params || {})
        }
        const res = await fetch(`${this.url}/${action}`,options)
        if (!res.ok) {
            fail(`${res.status} ${res.statusText}`)
        }
        const json = await res.json()
        return json
    }


    async login(username:string,password:string):Promise<void> {
        const options:RequestInit = {
            method: 'POST',
            cache: 'no-cache',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },            
            body: new URLSearchParams({username,password})
        }
        const res = await fetch(`${this.url}/auth/login`,options)
        if (!res.ok) {
            fail(`${res.status} ${res.statusText}`)
        }
        // const json = await res.json()
        // if (typeof(json) !== 'object' && json.access_token === undefined)
        //     fail('invalid response')
        // this.token = json.access_token    
        this.token = new Date().toISOString()
    }

    async logout() {
        this.token = undefined
    }

    isLoggedIn() {
        return this.token !== undefined
    }

}