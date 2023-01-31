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
import { createElement } from "./Utils";

// interface CustomEventMap {
//     "pushpage": CustomEvent<number>;
// }

// declare global {
//     interface Window { //adds definition to Document, but you can do the same with HTMLElement
//         addEventListener<K extends keyof CustomEventMap>(type: K,
//            listener: (this: Window, ev: CustomEventMap[K]) => void): void;
//         dispatchEvent<K extends keyof CustomEventMap>(ev: CustomEventMap[K]): void;
//     }
// }


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

        const header = this.root.querySelector<HTMLElement>('.page-header')!
        const caption = this.root.querySelector<HTMLElement>('.page-caption')!
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

        window.addEventListener('popstate', () => {
            const m = location.pathname.match(/\/(\d+)/)
            if (!m) return
            const kod = parseInt(m[1])
            if (isNaN(kod)) return 
             viewModel.loadPage(kod)
        })

        viewModel.on('change:kod',() => {
            const {kod} = viewModel
            const url = kod ? `/${kod}` : '/'
            history.pushState(null,'',url)
        })

        // viewModel.on('change:workspace',() => {
        //     const {workspace} = viewModel
        //     const view = this.getWorkspaceView(workspace)
        //     if (workspace) {
        //         workspace.on('change:pic',() => {
        //             const {pic} = workspace
        //             const url = (pic) ? new URL(`../img/${pic}`,import.meta.url) : ''
        //             const backgroundImage = (url) ? `url(${url})` : ''
        //             this.root.querySelector<HTMLElement>('.pic-m1')!.style.backgroundImage = backgroundImage
        //         })
        //     }
        //     if (view)
        //         this.root.querySelector('.workspace')!.replaceChildren(view.root)
        //     else
        //         this.root.querySelector('.workspace')!.replaceChildren()
        // })

        //viewModel.login('adm','adm').then(() => viewModel.loadPage(1))

        viewModel.on('change:page',() => {
            const {font=16,css=[],background} = viewModel.page?.design || {}
            document.documentElement.style.setProperty('--font-size', `${font}px`);
            const links = css.map(it => createElement(`<link data-css rel="stylesheet" type="text/css" href="/data/${it}">`))
            document.head.querySelectorAll('link[data-css]').forEach(it => it.remove())
            document.head.append(...links)
            if (background)
                document.body.style.backgroundImage = `url('/data/${background}')`
            else
                document.body.style.removeProperty('background-image')
            document.documentElement.style.setProperty('--top-menu',`${caption.offsetTop + 10}px`)
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