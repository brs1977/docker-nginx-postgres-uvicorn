import { fragment, h } from "../core/dom";
import { link } from "../core/html";

export function header() {
    let is_active = false
    //let $up: HTMLLinkElement
    let $down: HTMLLinkElement
    function onclick(e:Event) {
        e.preventDefault()
        e.stopPropagation()
        is_active = !is_active
        $el.classList.toggle('header--active',is_active)
        //$up.classList.toggle('expand-link--active',!is_active)
        $down.classList.toggle('expand-link--active',is_active)
    }
    const $el = h('header.header',{onclick},
        h('header.header__title','Заголовок'),
        //$up = link({className:'header__link  expand-link expand-link--up expand-link--active',onclick}),
        $down = link({className:'header__link expand-link expand-link--down',onclick}),
    )
    return $el
}

export function footer() {
    let is_active = false
    let $up: HTMLLinkElement
    //let $down: HTMLLinkElement
    function onclick(e:Event) {
        e.preventDefault()
        e.stopPropagation()
        is_active = !is_active
        $el.classList.toggle('footer--active',is_active)
        $up.classList.toggle('expand-link--active',is_active)
        //$down.classList.toggle('expand-link--active',!is_active)
    }
    const $el = h('footer.footer',{onclick},
        h('footer.footer__title','Подвал'),
        $up = link({className:'footer__link  expand-link expand-link--up',onclick}),
        //$down = link({className:'footer__link expand-link expand-link--down expand-link--active',onclick}),
    )
    return $el
}

export function sidebar() {
    let is_active = false
    // let $left: HTMLLinkElement
    let $right: HTMLLinkElement
    function onclick(e:Event) {
        e.preventDefault()
        e.stopPropagation()
        is_active = !is_active
        $el.classList.toggle('sidebar--active',is_active)
        // $left.classList.toggle('expand-link--active',!is_active)
        $right.classList.toggle('expand-link--active',is_active)
    }
    const $el = h('aside.sidebar',{onclick},
        h('sidebar.sidebar__title','Меню'),
        // $left = link({className:'sidebar__link  expand-link expand-link--left expand-link--active',onclick}),
        $right = link({className:'sidebar__link expand-link expand-link--right',onclick}),
    )
    return $el
}

export function main() {
    return fragment(
        header(),
        sidebar(),
        h('main.main'),
        footer()
    )
    // return h('main.main',
    //     header(),
    //     // sidebar(),
    //     // footer()
    // )
}