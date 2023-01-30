import { Page } from "./models/Page";
import { isPage } from "./models/Page.guard";
import { createSettings, PageModel, API, Settings } from "./PageTypes";
import { FailError } from "./Utils";

export class PageModelAPI implements PageModel {

    static SETTINGS = 'SETTINGS'
    private settings = createSettings()
    private isLoggedIn = false

    constructor(readonly api: API) { }

    // async loadMenu(): Promise<Menu> {
    //     return this.api.get<Menu>('menu');
    //     return []
    // }

    async loadSettings(): Promise<Settings> {
        if (!this.isLoggedIn)
            return this.settings
        let settings = createSettings()
        try {
            const s = localStorage.getItem(PageModelAPI.SETTINGS)
            if (s) {
                const obj = JSON.parse(s)
                if (typeof (obj) === 'object')
                    settings = { ...settings, ...obj }
            }
        } catch (e) {
            console.log('loadSettings', e)
        }
        return settings
    }

    async login(username: string, password: string) {
        await this.api.login(username, password)
        this.isLoggedIn = true
    }

    // async loadUser(): Promise<User> {
    //     return this.api.get<User>('auth/me')
    // }

    async saveSettings(settings: Settings): Promise<Settings> {
        if (this.isLoggedIn)
            localStorage.setItem(PageModelAPI.SETTINGS, JSON.stringify(settings))
        else
            this.settings = settings
        return settings
    }

    async logout() {
        await this.api.logout()
    }

    // async loadWorkspace<T extends WorkspaceProps>(kod: number) {
    //     return await this.api.get<T>(`menu/${kod}`)
    // }

    async loadPage(kod:number):Promise<Page> {
        const obj = await this.api.get<unknown>(`page/${kod}`)
        console.log('loadPage',obj,isPage(obj))
        if (isPage(obj))
            return obj
        else {
            const s = `wrong page ${kod}`
            console.log(s,obj)
            throw new FailError(s)
        }
    }

    // async loadTools(kod:number) {
    //     return await this.api.get<Tools>(`menu/${kod}/ins`)
    // }


} 