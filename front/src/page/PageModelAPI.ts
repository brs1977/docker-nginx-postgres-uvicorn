import { createSettings, Menu, PageModel, API, Settings, User, WorkspaceProps, WorkspaceMainProps } from "./PageTypes";

export class PageModelAPI implements PageModel {

    static SETTINGS = 'SETTINGS'
    private settings = createSettings()
    private isLoggedIn = false
   
    constructor(readonly api: API) {}
    
    async loadMenu(): Promise<Menu> {
        return this.api.get<Menu>('config/menu');
    }

    async loadSettings(): Promise<Settings> {
        if (!this.isLoggedIn)
            return this.settings
        let settings = createSettings()
        try {
            const s = localStorage.getItem(PageModelAPI.SETTINGS)
            if (s) {
                const obj = JSON.parse(s) 
                if (typeof(obj) === 'object')
                settings = {...settings,...obj}
            }
        } catch (e) {
            console.log('loadSettings',e)
        }
        return settings
    }

    async login(username:string,password:string) {
        await this.api.login(username,password)
        this.isLoggedIn = true
    }

    async loadUser(): Promise<User> {
        return this.api.get<User>('users/me')
    }

    async saveSettings(settings: Settings): Promise<Settings> {
        if (this.isLoggedIn)
            localStorage.setItem(PageModelAPI.SETTINGS,JSON.stringify(settings))
        else
            this.settings = settings
        return settings
    }

    async logout() { 
        await this.api.logout()
    }

    async loadWorkspace(kod: number) {
        //return await this.api.get<WorkspaceProps>(`config/menu/${kod}/`)
        const props: WorkspaceMainProps = {page: 1, type: 1}
        return props
    }

    
} 