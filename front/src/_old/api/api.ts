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

export type AlertAction = {
    type:'alert',
    title: string,
    text: string
}

export type PageAction = {
    type: 'page'
}

export type Action = AlertAction | PageAction

export type MenuItem = {
    kod:number,
    parent:number,
    name:string,
    action?: Action
}
export function is_alert_action(arg?: Action): arg is AlertAction {
    return arg !== undefined && arg.type == 'alert'
}

export function is_page_action(arg?: Action): arg is PageAction {
    return arg !== undefined && arg.type == 'page'
}

export type Menu = Array<MenuItem>

export type Settings = {
    caption: boolean
    sidebar: boolean
    footer: boolean
}

export interface API {
    users():Promise<Users>
    login(username:string,password:string):Promise<void>
    logout():Promise<void>
    me():Promise<User>
    on(event:string,callback:Function):Function
    menu(): Promise<Menu>
    settings(): Promise<Settings>
    settings_change(settings:Partial<Settings>):Promise<Settings>
    // page(kod:number):Promise<string>
}