import { showAlert } from "./Dialogs";
import { Head } from "./models/Head";
import { MenuItem } from "./models/MenuItem";
import { getMenuChildren, getMenuTop } from "./PageTypes";
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
                    <span id="orgstr"></span>
                </div>
                <div class="caption-item caption-item-nav">
                    <span class="caption-item-title">Страница:</span>
                    <span id="brod"></span>
                </div>
            </div>
        </div>
        `)
        viewModel.on('change:page',() => {
            const head = viewModel.page?.head
            this.renderMenu(head)
            const {orgstr='',brod=''} = head?.ins ?? {}
            this.root.querySelector('#orgstr')!.textContent = orgstr ?? ''
            this.root.querySelector('#brod')!.textContent = brod ?? ''
        })

        // viewModel.on('change:tools',() => {
        //     const {tools} = viewModel
        //     this.root.querySelector('#ins1')!.textContent = tools?.ins1 ?? ''
        //     this.root.querySelector('#ins2')!.textContent = tools?.ins2 ?? ''
        // })

        // viewModel.on('change:kod',() => {
        //     this.root.querySelectorAll<HTMLElement>('.caption-menu-item[data-page]').forEach(it => {
        //         it.classList.toggle('caption-menu-active',it.dataset.page == viewModel.kod)
        //     })
        // })
    }

    renderMenu(head?:Head) {
        const menu = head?.menu ?? []
        const items = getMenuTop(menu)
            .map(it => {
                if (it.typ_menu == 'sub') {
                    const children = getMenuChildren(menu,it.kod)
                    return this.renderDropDownItem(it,children)
                }
                else /*(isPageAction(it.action))*/
                    return this.renderItem(it)
            })
        this.root.querySelector('.caption-menu')?.replaceChildren(...items)
        this.root.querySelectorAll<HTMLElement>('.caption-menu-item').forEach(it => {
            it.classList.toggle('caption-menu-active',it.dataset.kod == head?.active_menu)
        })
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
        <div class="caption-menu-item dropdown" tabindex="1" data-id="${item.kod}">
            <i class="dropdown-content" tabindex="1"></i>
            <a class="dropdown-button">${item.name}</a>
            <ul class="dropdown-menu"></ul>
        </div>  
        `)
        el.querySelector<HTMLElement>('.dropdown-menu')!.append(...childNodes)  
        return el          
    }

    renderItem(item:MenuItem) {
        const page = item.typ_menu === 'ref' ? item.ref : 0
        const el = createElement<HTMLLinkElement>(/*html*/`<a href="/${page}" data-kod="${item.kod}" class="caption-menu-item">${item.name}</a>`)
        this.setupItem(item,el)
        return el
    }

    setupItem(item:MenuItem,el:HTMLLinkElement) {
        if (item.typ_menu === 'alert') {
            const {title='Заголовок',text='Сообщение'} = item.alert ?? {}
            el.addEventListener('click',(e) => {
                e.preventDefault()
                showAlert({
                    title,
                    text
                })
            })
        } else if (item.typ_menu === 'ref') {
            const page = item.ref ?? 0
            el.addEventListener('click', e => {
                e.preventDefault()
                this.viewModel.loadPage(page)
            })
        } else {
            el.addEventListener('click', e => {
                e.preventDefault()
                showAlert({title: 'Ошибка', text:`Не задано действие для kod:${item.kod}`})
            })
        }
    }

}