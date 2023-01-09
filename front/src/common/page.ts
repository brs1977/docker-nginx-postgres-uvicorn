import { h } from "../core/dom"
import { input, label, link } from "../core/html"

export type PageProps = {
    sidebar?: Node
}

function add(parent:Node|null,child?:Node) {
    console.log(parent,child)
    if (parent && child)
        parent.appendChild(child)
}

export function page(props?:PageProps) {
    let header: HTMLElement
    let sidebar_toggle: HTMLElement
    let caption: HTMLElement
    let sidebar: HTMLElement
    //let sidebar_close: HTMLElement
    let caption_checkbox: HTMLInputElement
    let footer_checkbox: HTMLInputElement
    let footer: HTMLElement
    const page = h('div.page',
        header = h('div.page-header',
        sidebar_toggle = link({href:'#', className:"icon icon-hamburger"}),
            h('div.page-header-title','Заголовок')
        ),
        caption = h('div.page-caption page-caption-show',
            h('div.page-caption-inner',
                h('div.page-caption-title','Шапка')
            )
        ),
        h('div.page-main',
            sidebar = h('div.page-sidebar page-sidebar-show',
                h('div.page-sidebar-inner',
                    h('div.page-sidebar-header',
                        h('div.page-sidebar-title',
                            label({className:'page-sidebar-checkbox'},
                                h('span','Шапка '),
                                caption_checkbox = input({name:'header',type:'checkbox',checked:true})
                            ),
                            label({className:'page-sidebar-checkbox'},
                                h('span','Подвал '),
                                footer_checkbox = input({name:'footer',type:'checkbox',checked:true})
                            ),
                        ),
                        //sidebar_close = link({href:'#',className:'icon icon-close'}),
                    ),
                    h('div.page-sidebar-content'),
                    h('div.page-sidebar-footer'),
                )
            ),
            h('div.page-workspace',
                h('div.page-workspace-inner','Рабочая область')
            )
        ),
        footer = h('div.page-footer page-footer-show',
            h('div.page-footer-inner','Подвал')
        )
    )

    sidebar_toggle.addEventListener('click', (e) => {
        e.preventDefault()
        sidebar.classList.toggle('page-sidebar-show')
    })
    // sidebar_close.addEventListener('click',(e) => {
    //     e.preventDefault()
    //     sidebar.classList.remove('page-sidebar-show')
    // })
    caption_checkbox.addEventListener('change',() => {
        caption.classList.toggle('page-caption-show',caption_checkbox.checked)
    })
    footer_checkbox.addEventListener('change',() => {
        footer.classList.toggle('page-footer-show',footer_checkbox.checked)
    })
    caption_checkbox.checked = true
    footer_checkbox.checked = true

    if (props) {
        add(sidebar.querySelector('.page-sidebar-content'),props.sidebar)
    }

    return page

}