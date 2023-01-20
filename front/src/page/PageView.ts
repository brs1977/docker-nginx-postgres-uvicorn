import { PageCaptionView } from "./PageCaptionView";
import { PageHeaderView } from "./PageHeaderView";
import { PageViewModel } from "./PageViewModel";
import { View } from "./View";
import { PageSidebarView } from "./PageSidebarView";
import { PageFooterView } from "./PageFooterView";
import { WorkspaceMainViewModel } from "./workspaces/WorkspaceMainViewModel";
import { WorkspaceMainFragment } from "./workspaces/WorkspaceMainFragment";
import { WorkspaceProps } from "./PageTypes";
import { WorkspaceViewModel } from "./workspaces/WorkspaceViewModel";

interface CustomEventMap {
    "pushpage": CustomEvent<number>;
}

declare global {
    interface Window { //adds definition to Document, but you can do the same with HTMLElement
        addEventListener<K extends keyof CustomEventMap>(type: K,
           listener: (this: Window, ev: CustomEventMap[K]) => void): void;
        dispatchEvent<K extends keyof CustomEventMap>(ev: CustomEventMap[K]): void;
    }
}


export class PageView extends View<HTMLDivElement> {

    constructor(readonly viewModel: PageViewModel) {
        super(/*html*/`
            <div class="page">
                <div class="page-header"></div>
                <div class="page-caption"></div>
                <div class="page-main">
                    <div class="page-sidebar"></div>
                    <div class="page-workspace">
                        <div class="div-work pic-m1">
                        </div>
                        <div class="workspace">
                        </div>
                    </div>
                </div>            
                <div class="page-footer page-footer-show"></div>
            </div>
        `)

        const header = this.root.querySelector('.page-header')!
        const caption = this.root.querySelector('.page-caption')!
        const sidebar = this.root.querySelector('.page-sidebar')!
        const footer = this.root.querySelector('.page-footer')!
        
        header.appendChild(new PageHeaderView(viewModel).root)
        caption.appendChild(new PageCaptionView(viewModel).root)
        sidebar.appendChild(new PageSidebarView(viewModel).root)
        footer.appendChild(new PageFooterView().root)

        viewModel.on('change:settings',() => {
            const {settings} = viewModel
            caption.classList.toggle('page-caption-show',settings.caption)
            sidebar.classList.toggle('page-sidebar-show',settings.sidebar)
            footer.classList.toggle('page-footer-show',settings.footer)
        })

        
        window.addEventListener('pushpage', e => {
            viewModel.loadPage(e.detail)
            history.pushState(null,'',`/${e.detail}`)
        })

        window.addEventListener('popstate', () => {
            if (!viewModel.user) return
            const m = location.pathname.match(/\/(\d+)/)
            if (!m) return
            const kod = parseInt(m[1])
            if (isNaN(kod)) return 
             viewModel.loadPage(kod)
        })

        viewModel.on('change:workspace',() => {
            const {workspace} = viewModel
            const view = this.getWorkspaceView(workspace)
            if (view)
                this.root.querySelector('.workspace')!.replaceChildren(view.root)
            else
                this.root.querySelector('.workspace')!.replaceChildren()
        })

    }


    getWorkspaceView(viewModel?:WorkspaceViewModel<WorkspaceProps>) {
        if (viewModel instanceof WorkspaceMainViewModel) {
            return new WorkspaceMainFragment(viewModel)
        } else {
            return undefined
        }
    }


}