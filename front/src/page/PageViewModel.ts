import { Menu, PageModel, Settings, User } from "./PageTypes"
import { Props, ViewModel } from "./ViewModel"

type PageProps = Props & {  
    settings: Settings,
    menu: Menu,
    user?: User 
}
export class PageViewModel extends ViewModel<PageProps>{

    
    constructor(readonly model:PageModel) {
        super()
    }

    changeSettings(partial:Partial<Settings>) {
        const settings = {...this.settings,...partial}
        this.model.saveSettings(settings)
        this.setProps({settings})
    }

    async login(username:string,password:string) {
        await this.model.login(username,password)
        const [settings,menu,user] = await Promise.all([
            this.model.loadSettings(),
            this.model.loadMenu(),
            this.model.loadUser()
        ])
        this.setProps({
            settings,
            menu,
            user
        })
    }

    async logout() {
        await this.model.logout()
        const settings = await this.model.loadSettings()
        this.setProps({
            settings,
            menu: [],
            user: undefined
        })
    }

    get settings() { 
        return this.getProp('settings') ?? {caption: true, footer: true, sidebar: true } 
    }
    
    get menu() { return this.getProp('menu') || [] }

    get user() { return this.getProp('user') }

}