import { showAlert } from "./Dialogs";
import { isAlertAction, isPageAction, Menu, MenuItem } from "./PageTypes";
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
                    объект оргструктуры не выбран
                </div>
                <div class="caption-item caption-item-nav">
                    <span class="caption-item-title">Страница:</span>
                    Ввод / Администрирование / Настройка / Справочники 
                </div>
            </div>
        </div>
        `)
        viewModel.on('change:menu',() => this.renderMenu(viewModel.menu))
    }

    renderMenu(menu:Menu) {
        const items = menu
            .filter(it => it.parent == 0)
            .sort((a,b) => a.kod - b.kod)
            .map(it => {
                const children = menu.filter(child => it.kod === child.parent)
                if (children.length)
                    return this.renderDropDownItem(it,children)
                else
                    return this.renderItem(it)
            })
        this.root.querySelector('.caption-menu')?.replaceChildren(...items)
    }

    renderDropDownItem(item:MenuItem,children:Array<MenuItem>) {
        const childNodes = children.sort((a,b) => a.kod - b.kod)
            .map(child => {
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
        const el = createElement<HTMLLinkElement>(/*html*/`<a href="/${item.kod}" class="caption-menu-item">${item.name}</a>`)
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
            el.addEventListener('click', e => {
                e.preventDefault()
                window.dispatchEvent(new CustomEvent<number>('pushpage',{detail: item.kod}))
            })
        } else {
            el.addEventListener('click', e => {
                e.preventDefault()
                showAlert({title: 'Ошибка', text:`Не задано действие для kod:${item.kod}`})
            })
        }
    
    }

}