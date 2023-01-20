import { PageCaptionView } from "./PageCaptionView";
import { PageHeaderView } from "./PageHeaderView";
import { PageViewModel } from "./PageViewModel";
import { View } from "./View";
import { PageSidebarView } from "./PageSidebarView";
import { PageFooterView } from "./PageFooterView";

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
            console.log('change:settings',settings)
            caption.classList.toggle('page-caption-show',settings.caption)
            sidebar.classList.toggle('page-sidebar-show',settings.sidebar)
            footer.classList.toggle('page-footer-show',settings.footer)
        })
    }

}