import { WorkspaceMainViewModel } from "./workspaces/WorkspaceMainViewModel"
import { PageModel, Props, Settings, WorkspaceProps } from "./PageTypes"
import { ViewModel } from "./ViewModel"
import { Page } from "./models/Page"

type PageProps = Props & {  
    kod: number,
    page: Page,
    settings: Settings,
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
        await this.loadPage(101)
    }

    getWorkspace(props:WorkspaceProps) {
        switch(props.type) {
            case 1: return new WorkspaceMainViewModel(props)
            default: return undefined
        }
    }

    async loadPage(kod:number) {
        this.setProps({kod})
        const page = await this.model.loadPage(kod)
        this.setProps({page})
    }

    async logout() {
        await this.model.logout()
        this.loadPage(0)
    }

    get settings() { 
        return this.getProp('settings') ?? {caption: true, footer: true, sidebar: true } 
    }

    get page() { return this.getProp('page') }
    
    // get menu() { return this.getProp('menu') || [] }

    // get user() { return this.getProp('user') }

    // get workspace() { return this.getProp('workspace') }

    // get tools() { return this.getProp('tools') }

    get kod() { return this.getProp('kod') }

}