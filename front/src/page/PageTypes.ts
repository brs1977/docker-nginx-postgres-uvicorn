import { MenuItem } from "./models/MenuItem"
import { Page } from "./models/Page"

export type Props = {}

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

// export type AlertAction = {
//     type:'alert',
//     title: string,
//     text: string
// }

// export type PageAction = {
//     type: 'page',
//     page: number,
// }

// export type Action = AlertAction | PageAction

// // export type MenuItem = {
// //     kod:number,
// //     kod_parent:number,
// //     name:string,
// //     action?: Action
// // }
// export function isAlertAction(arg?: Action): arg is AlertAction {
//     return arg !== undefined && arg.type == 'alert'
// }

// export function isPageAction(arg?: Action): arg is PageAction {
//     return arg !== undefined && arg.type == 'page'
// }

export function createSettings(partial?:Partial<Settings>) {
    return {caption:true,footer:true,sidebar:true,...partial ?? {}}
}

function sortMenu(a:MenuItem,b:MenuItem) {
    return a.kod - b.kod
}

export function getMenuTop(menu:Array<MenuItem>) {
    return menu.filter(it => it.kod_parent === 0).sort(sortMenu)
}

export function getMenuChildren(menu:Array<MenuItem>,parent:number) {
    return menu.filter(it => it.kod_parent == parent).sort(sortMenu)
}


export type Settings = {
    caption: boolean
    sidebar: boolean
    footer: boolean
}

export type WorkspaceCustomProps = Props & {
    kod: number,
    pic?: string,
}

export type WorkspaceMainProps = WorkspaceCustomProps & {
    type: 1,
    title: string,
    picpic: 0 | string,
    n_par: Array<number>,
    m_par: Array<{
        pic:string,
        txt:string
    }>
}

export type WorkspaceInputProps = WorkspaceCustomProps & {
    type: 2
}

export type Tools = {
    ins1: string,
    ins2: string
}

export type WorkspaceProps = WorkspaceMainProps | WorkspaceInputProps

export interface PageModel {
    // loadMenu(): Promise<Menu>
    loadSettings(): Promise<Settings>
    // loadUser(): Promise<User>
    saveSettings(settings:Settings):Promise<Settings>
    login(username:string,password:string):Promise<void>
    logout(): Promise<void>
    // loadWorkspace(kod:number):Promise<WorkspaceProps>
    // loadTools(kod:number): Promise<Tools>
    loadPage(kod:number):Promise<Page>
}


export interface API {
    get<T>(action:string,params?:any):Promise<T> 
    post<T>(action:string,params?:any):Promise<T> 
    login(username:string,password:string):Promise<void>
    logout():Promise<void>
}
