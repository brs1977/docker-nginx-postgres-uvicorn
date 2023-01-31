import { PageViewModel } from "./PageViewModel"
import { View } from "./View"
import { PageLoginView } from "./PageLoginView"
import { PageLogonView } from "./PageLogonView"
import { PageHelpView } from "./PageHelpView"

export class PageSidebarView extends View<HTMLDivElement> {

    constructor(viewModel:PageViewModel) {
        super(/*html*/`
            <div class="sidebar">
                <div class="sidebar-header">
                    <label class="sidebar-checkbox">
                        <span class="sidebar-checkbox-label">Главное Меню</span>
                        <input class="sidebar-checkbox-input" name="caption" type="checkbox">
                    </label>
                    <label class="sidebar-checkbox sidebar-checkbox-footer">
                        <span class="sidebar-checkbox-label">Подвал</span>
                        <input class="sidebar-checkbox-input" name="footer" type="checkbox">
                    </label>
                    <div class="sidebar-close"><img class="sidebar-close-img" src="/data/close.svg"></div>
                </div>
                <div class="sidebar-items"></div>
        </div>
        `)

        const caption = this.root.querySelector<HTMLInputElement>('input[name=caption')!
        const footer = this.root.querySelector<HTMLInputElement>('input[name=footer')!
        const sidebar = this.root.querySelector<HTMLInputElement>('.sidebar-items')!

        caption.addEventListener('change', () => {
            viewModel.changeSettings({caption:caption.checked})
        })

        footer.addEventListener('change',() => {
            viewModel.changeSettings({footer: footer.checked})
        })

        this.root.querySelector('.sidebar-close')?.addEventListener('click', e => {
            e.preventDefault()
            viewModel.changeSettings({sidebar: false})
        })

        viewModel.on('change:settings',() => {
            const {settings} = viewModel
            caption.checked = settings.caption
            footer.checked = settings.footer
        })

        const login = new PageLoginView(viewModel)

        const logon = new PageLogonView(viewModel)

        const help = new PageHelpView()

        viewModel.on('change:page',() => {
            this.root.querySelector('.sidebar-header')!.classList.toggle('sidebar-header-hide',!viewModel.page?.design.checkbox)
            if (viewModel.page?.sidebar.user)
                sidebar.replaceChildren(logon.root,help.root)
            else
                sidebar.replaceChildren(login.root,help.root)
        })

    }
}
