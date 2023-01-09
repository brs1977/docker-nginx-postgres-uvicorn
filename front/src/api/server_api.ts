import { events } from "../core/events";
import { fail } from "../core/utils";
import { API, Users, User } from "./api";

export function get_url(pathname:string,port:number,server_url?:string) {
    const url = new URL(server_url ?? location.toString())
    url.pathname = pathname
    url.port = '' + port
    return url.toString()
}

export function server_api(url:string):API {
    
    //const url = get_url(base,port,server_url)

    const ev = events()

    let access_token: string | undefined = undefined


    async function get<T>(action:string,params?:any):Promise<T> {
        const $url = new URL(`${url}/${action}`)
        if (params)
            $url.search = new URLSearchParams(params).toString()
        const options:RequestInit = {
            method: 'GET',
            //mode: 'same-origin',
            //cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            // credentials: 'omit', // include, *same-origin, omit
            headers: {
               'Content-Type': 'application/json',
            //    "Sec-Fetch-Dest": "empty",
            //    "Sec-Fetch-Mode": "no-cors",
            //    "Sec-Fetch-Site": "same-site"
              // 'Content-Type': 'application/x-www-form-urlencoded',
              ...(access_token ? {'Authorization': `Bearer ${access_token}`} : {})
            },            
        }
        const res = await fetch($url,options)
        if (!res.ok) {
            fail(`${res.status} ${res.statusText}`)
        }
        const json = await res.json()
        return json
    }


    // async function post<T>(action:string,props?:FetchProps):Promise<T> {
    //     const options:RequestInit = {
    //         method: 'POST',
    //         mode: 'cors',
    //         cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    //         //credentials: 'omit', // include, *same-origin, omit
    //         headers: {
    //            'Content-Type': 'application/json',
    //           // 'Content-Type': 'application/x-www-form-urlencoded',
    //         },            
    //         body: JSON.stringify(params || {})
    //     }
    //     const res = await fetch(`${url}${action}`,options)
    //     if (!res.ok) {
    //         fail(`${res.status} ${res.statusText}`)
    //     }
    //     const json = await res.json()
    //     return json
    // }

    async function users():Promise<Users> {
        const users = await get<Users>('users/')
        return users
    }

    async function login(username:string,password:string) {
        // const body = new FormData()
        // body.append('username',username)
        // body.append('password',password)
        const options:RequestInit = {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },            
            body: new URLSearchParams({username,password})
        }
        const res = await fetch(`${url}/login`,options)
        if (!res.ok) {
            fail(`${res.status} ${res.statusText}`)
        }
        const json = await res.json()
        if (typeof(json) !== 'object' && json.access_token === undefined)
            fail('invalid response')
        access_token = json.access_token
        ev.emit('login')
    }

    async function me(): Promise<User> {
        return get<User>('users/me')
    }

    async function logout():Promise<void> {
        access_token = undefined
        ev.emit('logout')
    }


    return {
        users,
        login,
        logout,
        me,
        on: ev.on
    }
}