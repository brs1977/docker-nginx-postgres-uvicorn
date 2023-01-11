import { API } from "../api/api"
import { page } from "../common/page"
import {  cleanup, h } from "../core/dom"
import { button, form, img, input, link } from "../core/html"

type LoginParams = {
    api: API
}

function login({api}:LoginParams) {
    let $username: HTMLInputElement
    let $password: HTMLInputElement
    async function onsubmit(e:Event) {
        e.preventDefault()
        const username = $username.value
        const password = $password.value
        await api.login(username,password)
    }
    const f = form({className: 'login',onsubmit},
        h('div.login-header',
            link({href:'#'},'регистрация'),
            h('span','|'),
            link({href:'#', className: 'login-forgot'},'забыли пароль?')
        ),
        h('div.login-data',
            h('div.login-title','Вход'),
            $username = input({className:'login-input'}),
            $password = input({className:'login-input',type:'password'}),
            button({className:'login-button'},'ОК')
        )
    )
    return f
}

type LogonParams = {
    api: API
}


function logon({api}:LogonParams) {
    
    let $username: HTMLElement
    let $tabs: HTMLElement

    async function onclick(e:Event) {
        e.preventDefault()
        await api.logout()
    }

    function show_tab(e:Event) {
        e.preventDefault()
        const arr = Array.from($tabs.querySelectorAll<HTMLElement>('.logon-tab'))
        const index = arr.findIndex(el => el === e.target)
        arr.forEach( tab => {
            tab.classList.toggle('logon-tab-active',tab === e.target)
        })
        $tabs.querySelectorAll<HTMLElement>('.logon-tab-data').forEach( (data,data_index) => {
            data.classList.toggle('logon-tab-data-active',index == data_index)
        })
    }

    function toggle_node(e:Event) {
        const el = (e.target as HTMLElement)
        el.classList.toggle('logon-tree-node-active')
        el.nextElementSibling?.classList.toggle('logon-tree-items-active')
    }

    const el = h('div.logon logon-hide',
        h('hr.logon-line'),
        h('div.logon-header',
            h('div.logon-title','Навигация'),
            link({href:'#',className:'icon icon-back'}),
            link({href:'#',className:'icon icon-forward'}),
            link({href:'#',className:'icon icon-down'}),
            link({href:'#',className:'icon icon-up'}),
        ),
        h('hr.logon-line'),
        h('div.logon-data',
            h('div.login-label','логин:'),
            $username = h('div.login-value','значение'),
            h('div.login-label','статус:'),
            h('div.login-value','значение'),
            h('div.login-label','в системе:'),
            h('div.login-value','ЧЧ:ММ:CC')
        ),
        h('hr.logon-line'),
        h('div.logon-footer',
            link({href:'#'},'Кабинет'),
            link({href:'#',onclick},'Выйти')
        ),
        h('div.logon-short', 'Тут краткое описание (1-2 предложения) текущей страницы'),
        $tabs = h('div',
            h('div.logon-tabs',
                h('div.logon-tab',{onclick:show_tab},'Помощь'),
                h('div.logon-tab',{className:'logon-tab-active',onclick: show_tab}, 'Инструменты'),
            ),
            h('div.logon-tabs-data',
                h('ol.logon-help logon-tab-data logon-tab-data-active',
                    h('li.logon-help-item','Для начала работы необходимо авторизоваться(ввести логин и пароль)'),
                    h('li.logon-help-item','Главноне меню(Шапка) и дополнительная информация(Подвал) доступны в Боковой панели(см.выше)'),
                    h('li.logon-help-item','Подробная контекстная помощь - правый верхний угол страницы')
                ),
                h('ul.logon-tab-data logon-tree',
                    h('li.logon-tree-group',
                        h('div.logon-tree-node',{onclick: toggle_node},'Входящие'),
                        h('ul.logon-tree logon-tree-items',
                            h('li.logon-tree-item',h('i.icon icon-tree'),h('span','Исходящие')),
                            h('li.logon-tree-item',h('i.icon icon-tree'),h('span','Избранное')),
                            h('li.logon-tree-item',h('i.icon icon-tree'),h('span','Недавние документы'))
                        )
                    ),
                    h('li.logon-tree-group',
                        h('div.logon-tree-node',{onclick: toggle_node},'Общие папки'),
                        h('ul.logon-tree logon-tree-items',
                            h('li.logon-tree-item',h('i.icon icon-tree'),h('span','Договоры')),
                            h('li.logon-tree-item',h('i.icon icon-tree'),h('span','Компания')),
                        )
                    )
                )
            ),
        )
    )

    const dispose = api.on('login',async() => {
        const user = await api.me()
        $username.textContent = user.fio
    })
    cleanup(el,dispose)
    return el
}

export type MainParams = {
    api: API
}

export function main_page({api}:MainParams) {
    let $login: HTMLElement
    let $logon: HTMLElement
    const sidebar = h('div',
        $login = login({api}),
        $logon = logon({api})
    )
    const el = page({
        sidebar
    })
    const login_dispose = api.on('login', () => {
        $login.classList.add('login-hide')
        $logon.classList.remove('logon-hide')
    })
    const logon_dispose = api.on('logout',() => {
        $login.classList.remove('login-hide')
        $logon.classList.add('logon-hide')
    })
    cleanup(el,login_dispose)
    cleanup(el,logon_dispose)
    return el
}