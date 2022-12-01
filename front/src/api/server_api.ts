import { fail } from "../core/utils";
import { API, Users } from "./api";

export function get_url(port:number) {
    const url = new URL(location.toString())
    url.pathname = ''
    url.port = '' + port
    return url.toString()
}

export function server_api(port:number):API {
    
    const url = get_url(port)


    async function get<T>(action:string,params?:any):Promise<T> {
        const $url = new URL(`${url}${action}`)
        if (params)
            $url.search = new URLSearchParams(params).toString()
        const options:RequestInit = {
            method: 'GET',
            mode: 'same-origin',
            //cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'omit', // include, *same-origin, omit
            headers: {
               'Content-Type': 'application/json',
               "Sec-Fetch-Dest": "empty",
               "Sec-Fetch-Mode": "no-cors",
               "Sec-Fetch-Site": "same-site"
              // 'Content-Type': 'application/x-www-form-urlencoded',
            },            
        }
        const res = await fetch(`${url}${action}`,options)
        console.log(res)
        if (!res.ok) {
            fail(`${res.status} ${res.statusText}`)
        }
        const json = await res.json()
        return json
    }


    async function post<T>(action:string,params?:any):Promise<T> {
        const options:RequestInit = {
            method: 'POST',
            //mode: 'no-cors',
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            //credentials: 'omit', // include, *same-origin, omit
            headers: {
               'Content-Type': 'application/json',
              // 'Content-Type': 'application/x-www-form-urlencoded',
            },            
            body: JSON.stringify(params || {})
        }
        const res = await fetch(`${url}${action}`,options)
        console.log(res)
        if (!res.ok) {
            fail(`${res.status} ${res.statusText}`)
        }
        const json = await res.json()
        return json
    }

    async function users():Promise<Users> {
        const users = await get<Users>('users2')
        console.log('users',users)
        return users
    }

    return {
        users
    }
}