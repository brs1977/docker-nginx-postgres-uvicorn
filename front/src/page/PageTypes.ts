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
export function isAlertAction(arg?: Action): arg is AlertAction {
    return arg !== undefined && arg.type == 'alert'
}

export function isPageAction(arg?: Action): arg is PageAction {
    return arg !== undefined && arg.type == 'page'
}

export function createSettings(partial?:Partial<Settings>) {
    return {caption:true,footer:true,sidebar:true,...partial ?? {}}
}

export type Menu = Array<MenuItem>

export type Settings = {
    caption: boolean
    sidebar: boolean
    footer: boolean
}

export type WorkspaceCustomProps = Props & {
    page: number
}

export type WorkspaceMainProps = WorkspaceCustomProps & {
    type: 1
}

export type WorkspaceInputProps = WorkspaceCustomProps & {
    type: 2
}

export type WorkspaceProps = WorkspaceMainProps | WorkspaceInputProps

export interface PageModel {
    loadMenu(): Promise<Menu>
    loadSettings(): Promise<Settings>
    loadUser(): Promise<User>
    saveSettings(settings:Settings):Promise<Settings>
    login(username:string,password:string):Promise<void>
    logout(): Promise<void>
    loadWorkspace(kod:number):Promise<WorkspaceProps>
}


export interface API {
    get<T>(action:string,params?:any):Promise<T> 
    post<T>(action:string,params?:any):Promise<T> 
    login(username:string,password:string):Promise<void>
    logout():Promise<void>
}
