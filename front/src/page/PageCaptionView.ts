import { showAlert } from "./Dialogs";
import { getMenuChildren, getMenuTop, isAlertAction, isPageAction, Menu, MenuItem } from "./PageTypes";
import { PageViewModel } from "./PageViewModel";
import { createElement } from "./Utils";
import { View } from "./View";

export class PageCaptionView extends View<HTMLDivElement> {

    constructor(readonly viewModel:PageViewModel) {
        super(/*html*/`
        <div class="caption">
            <div class="caption-menu"></div>
            <div class="caption-items">
                <div class="caption-item caption-item-org">
                    <span class="caption-item-title">Локализация:</span>
                    <span id="ins1"></span>
                </div>
                <div class="caption-item caption-item-nav">
                    <span class="caption-item-title">Страница:</span>
                    <span id="ins2"></span>
                </div>
            </div>
        </div>
        `)
        viewModel.on('change:menu',() => this.renderMenu(viewModel.menu))

        viewModel.on('change:tools',() => {
            const {tools} = viewModel
            this.root.querySelector('#ins1')!.textContent = tools?.ins1 ?? ''
            this.root.querySelector('#ins2')!.textContent = tools?.ins2 ?? ''
        })

        viewModel.on('change:kod',() => {
            this.root.querySelectorAll<HTMLElement>('.caption-menu-item[data-page]').forEach(it => {
                it.classList.toggle('caption-menu-active',it.dataset.page == viewModel.kod)
            })
        })
    }

    renderMenu(menu:Menu) {
        const items = getMenuTop(menu)
            .map(it => {
                const children = getMenuChildren(menu,it.kod)
                if (children.length)
                    return this.renderDropDownItem(it,children)
                else (isPageAction(it.action))
                    return this.renderItem(it)
            })
        this.root.querySelector('.caption-menu')?.replaceChildren(...items)
    }

    renderDropDownItem(item:MenuItem,children:Array<MenuItem>) {
        const childNodes = children.map(child => {
            const el = createElement(/*html*/`
                <li class="dropdown-item">
                    <a class="dropdown-link" href="/${child.kod}">${child.name}</a>
                </li>
            `)
            this.setupItem(child,el.querySelector<HTMLLinkElement>('.dropdown-link')!)
            return el
        })
        const el = createElement(/*html*/`
        <div class="caption-menu-item dropdown" tabindex="1">
            <i class="dropdown-content" tabindex="1"></i>
            <a class="dropdown-button">${item.name}</a>
            <ul class="dropdown-menu"></ul>
        </div>  
        `)
        el.querySelector<HTMLElement>('.dropdown-menu')!.append(...childNodes)  
        return el          
    }

    renderItem(item:MenuItem) {
        const page = isPageAction(item.action) ? item.action.page : 0
        const el = createElement<HTMLLinkElement>(/*html*/`<a href="/${item.kod}" data-page="${page}" class="caption-menu-item">${item.name}</a>`)
        this.setupItem(item,el)
        return el
    }

    setupItem(item:MenuItem,el:HTMLLinkElement) {
        if (isAlertAction(item.action)) {
            const {title,text} = item.action
            el.addEventListener('click',(e) => {
                e.preventDefault()
                showAlert({
                    title,
                    text
                })
            })
        } else if (isPageAction(item.action)) {
            const {page} = item.action
            el.addEventListener('click', e => {
                e.preventDefault()
                this.viewModel.loadPage(page)
                // const cur = el.closest('.caption-menu-item')
                // el.closest('.page')?.querySelectorAll<HTMLElement>('.caption-menu-item').forEach(it => {
                //     it.classList.toggle('caption-menu-active',it == cur)
                // })
                // window.dispatchEvent(new CustomEvent<number>('pushpage',{detail: item.kod}))
            })
        } else {
            el.addEventListener('click', e => {
                e.preventDefault()
                showAlert({title: 'Ошибка', text:`Не задано действие для kod:${item.kod}`})
            })
        }
    
    }

}