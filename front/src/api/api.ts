export type User = {
    id: number,
    fio: string,
    email: string,
    username: string,
}

export type Users = Array<User>

export type Token = {
    access_token: string,
    token_type: string
}

export interface API {
    users():Promise<Users>
    login(username:string,password:string):Promise<void>
    logout():Promise<void>
    me():Promise<User>
    on(event:string,callback:Function):Function
}