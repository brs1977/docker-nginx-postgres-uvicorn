import { API } from "../api/api"
import { page } from "../common/page"
import {  cleanup, h } from "../core/dom"
import { button, form, input, link } from "../core/html"

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

    async function onclick(e:Event) {
        e.preventDefault()
        await api.logout()
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