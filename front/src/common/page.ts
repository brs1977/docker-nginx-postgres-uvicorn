import ham from '../img/ham.jpg'
import mess from '../img/mess.png'
import data from '../img/data.png'
import papka from '../img/papka.png'
import nastr from '../img/nastr.png'
import help2 from '../img/help2.png'
import shild from '../img/shild.png'
import close from '../img/close.svg'
import { make_element, make_fragment } from '../core/html'
import { show_alert } from '../core/alert'
import { API, is_alert_action, is_page_action, MenuItem, Settings } from '../api/api'
import { on } from '../core/dom'
import { make_page } from './pages'

export type PageProps = {
    api: API
}

function sort_menu (a:MenuItem,b:MenuItem) { return a.kod - b.kod }

function setup_actions(el:HTMLLinkElement,item:MenuItem) {
    if (is_alert_action(item.action)) {
        const {title,text} = item.action
        on(el,'click',(e) => {
            e.preventDefault()
            show_alert({
                title,
                text
            })
        })
    } else if (is_page_action(item.action)) {
        //console.log('page',item.kod)
        on(el,'click',async (e) => {
            e.preventDefault()
            const workspace = make_page(item.kod)
            const cur = el.closest('.caption-menu-item')
            el.closest('.page')?.querySelectorAll<HTMLElement>('.caption-menu-item').forEach(it => {
                it.classList.toggle('caption-menu-active',it == cur)
            })
            el.closest('.page')?.querySelector<HTMLElement>('.workspace')?.replaceChildren(workspace)
        })
        //page({api,root,workspace,is_caption:$caption_checkbox.checked,is_footer:$footer_checkbox.checked})
    }
}

type LoginProps = {
    api: API,
}

function login({api}:LoginProps) {
    const el = make_element(/*html*/`
        <form class="login">
            <div class="login-header">
                <a href="#">регистрация</a>
                <span>|</span>
                <a href="#" class="login-forgot">забыли пароль?</a>
            </div>
            <div class="login-data">
                <div class="login-title">Вход</div>
                <input class="login-input" name="username">
                <input class="login-input" type="password" name="password">
                <button class="login-button">ОК</button>
            </div>
        </form>
    `)
    on(el,'submit',async e => {
        e.preventDefault()
        const username = el.querySelector<HTMLInputElement>('input[name=username]')!.value
        const password = el.querySelector<HTMLInputElement>('input[name=password]')!.value
        await api.login(username,password)
    })
    api.on('login',() => {
        el.classList.add('login-hide')
    })
    api.on('logout',() => {
        el.classList.remove('login-hide')
    })
    return el
}

type LogonParams = {
    api: API
}

function logon({api}:LogonParams) {

    const el = make_element(/*html*/`
        <div class="logon">
        <div class="div-gran0 block" style="height:95px">юзер</div>
        <div class="div-gran0 block" style="height:72px">помошь</div>
            <div class="div-gran0 block" style="height:284px">панели</div>
        </div>
    `)
    api.on('login',() => {
        el.classList.add('logon-show')
    })
    api.on('logout',() => {
        el.classList.remove('logon-show')
    })
    return el
}

export function page({api}:PageProps) {

    function update_settings(settings: Settings) {
        $caption_checkbox.checked = settings.caption !== false
        $caption.classList.toggle('page-caption-show',$caption_checkbox.checked)
        $footer_checkbox.checked = settings.footer !== false
        $footer.classList.toggle('page-footer-show',$footer_checkbox.checked)
        $sidebar.classList.toggle('page-sidebar-show',settings.sidebar !== false) 
    }

    async function load() {
        const menu = await api.menu()
        const nodes = menu
        .filter(item => item.parent === 0)
        .sort(sort_menu)
        .map(item => {
            let el:HTMLElement
            const children = menu.filter(child => child.parent === item.kod)
            .sort(sort_menu)
            .map(child => {
                const el = make_element(/*html*/`
                    <li class="dropdown-item">
                        <a class="dropdown-link" href="#">${child.name}</a>
                    </li>
                `)
                setup_actions(el.querySelector<HTMLLinkElement>('.dropdown-link')!,child)
                return el
            })
            if (!children.length) {
                el = make_element(/*html*/`
                    <a href="#" class="caption-menu-item">${item.name}</a>
                `)
                setup_actions(el as HTMLLinkElement,item)
            }
            else {
                el = make_element(/*html*/`
                    <div class="caption-menu-item dropdown" tabindex="1">
                        <i class="dropdown-content" tabindex="1"></i>
                        <a class="dropdown-button">${item.name}</a>
                        <ul class="dropdown-menu"></ul>
                    </div>  
                `)
                el.querySelector<HTMLElement>('.dropdown-menu')!.append(...children)
            }
            return el
        })
        $caption.querySelector('.caption-menu')!.replaceChildren(...nodes)
    }
    const f = make_fragment(
        /*html*/
        `  <div class="page">
        <div class="page-header">
            <div class="header">
                <img class="header-hamburger" src="${ham}">
                <span class="header-title">Служба безопасности полетов авиации Вооруженных сил Российской Федерации</span>
                <div> <img class="shildik-own" src="${mess}" alt="Сообщения"> </div>
                <div> <img class="shildik-own" src="${data}" alt="Ввод данных"> </div>
                <div> <img class="shildik-own" src="${papka}" alt="Документы"> </div>
                <div> <img class="shildik-own" src="${nastr}" alt="Настройки"> </div>
                <div> <img class="shildik-own" src="${help2}" alt="Помощь"> </div>
                <div class="shildik-own">
                    <img class="shildik-own" src="${shild}" alt="Шильдик методологии">
                </div>
            </div>
        </div>
        <div class="page-caption page-caption-show">
            <div class="caption">
                <div class="caption-menu">
                    <!--
                    <div class="caption-menu-item caption-menu-active">Главная</div>
                    <div class="caption-menu-item">Ввод</div>
                    <div class="caption-menu-item dropdown" tabindex="1">
                            <i class="dropdown-content" tabindex="1"></i>
                            <a class="dropdown-button">Аналитика</a>
                            <ul class="dropdown-menu">
                                <li class="dropdown-item">
                                    <a class="dropdown-link" href="#">Мониторинг</a>
                                    <ul class="dropdown-submenu">
                                        <li><a class="dropdown-link" href="#">Готовность аэродромов</a></li>
                                        <li><a class="dropdown-link" href="#">Прогнозируемые метеоусловия на аэродромах</a></li>
                                        <li><a class="dropdown-link" href="#">План проведения летных смен</a></li>
                                        <li><a class="dropdown-link" href="#">Результаты летных смен</a></li>
                                        <li><a class="dropdown-link" href="#">Нарушения и ошибочные действия в ходе проведения летной смены</a></li>
                                        <li><a class="dropdown-link" href="#">Итоги летной деятельности</a></li>
                                        <li><a class="dropdown-link" href="#">Авиационные события</a></li>
                                        <li><a class="dropdown-link" href="#">Потери ВС</a></li>
                                        <li><a class="dropdown-link" href="#">Квалификация и уровень подготовки командиров экипажей</a></li>
                                    </ul>
                                </li>
                                <li class="dropdown-item"><a class="dropdown-link" href="#">Анализ</a></li>
                                <li class="dropdown-item">
                                    <a class="dropdown-link" href="#">Прогнозирование</a>
                                    <ul class="dropdown-submenu">
                                        <li><a class="dropdown-link" href="#">Прогноз динамики</a></li>
                                        <li><a class="dropdown-link" href="#">Данные</a></li>
                                    </ul>
                                </li>
                            </ul>
                    </div>
                    <div class="caption-menu-item">Данные</div>
                    <div class="caption-menu-item">ОФАС</div>
                    <div class="caption-menu-item">Документы</div>
                    <div class="caption-menu-item" id="alert-btn">Сообщение</div>
                    -->
                </div>
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
        </div>
        <div class="page-main">
            <div class="page-sidebar page-sidebar-show">
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
                        <img class="sidebar-close" src="${close}">
                    </div>
                    <div class="sidebar-items">
                    </div>
                </div>
            </div>
            <div class="page-workspace">
                <div class="div-work pic-m1">
                </div>
                <div class="workspace">
                </div>
            </div>
        </div>            
        <div class="page-footer page-footer-show">
            <div class="footer">
                <div class="footer-block">
                    Ваш аккаунт
                    <br>&nbsp;&nbsp;Войти
                    <br>&nbsp;&nbsp;Регистрация
                </div>
                <div class="footer-block">
                    О проекте
                </div>
                <div class="footer-block">
                    Контакты
                    <br>&nbsp;&nbsp;Связаться
                    <br>&nbsp;&nbsp;Добраться
                    <br>&nbsp;&nbsp;Официальный запрос 
                </div>
                <div class="footer-block">
                    Ростехприемка
                </div>
            </div>
        </div>
    </div>`
    )
    const $page = f.querySelector<HTMLElement>('.page')!
    const $hamburger = $page.querySelector<HTMLElement>('.header-hamburger')!
    const $caption = $page.querySelector<HTMLElement>('.page-caption')!
    const $sidebar = $page.querySelector<HTMLElement>('.page-sidebar')!
    const $caption_checkbox = $page.querySelector<HTMLInputElement>('.sidebar-checkbox input[name=caption]')!
    const $footer_checkbox = $page.querySelector<HTMLInputElement>('.sidebar-checkbox input[name=footer]')!
    const $sidebar_close = $page.querySelector<HTMLElement>('.sidebar-close')!
    const $sidebar_items = $page.querySelector<HTMLElement>('.sidebar-items')!
    // const $workspace = $page.querySelector<HTMLElement>('.page-workspace')!
    const $footer = $page.querySelector<HTMLElement>('.page-footer')!
    $hamburger.addEventListener('click', () => {
        $sidebar.classList.add('page-sidebar-show')
        api.settings_change({sidebar: true})
    })
    $caption_checkbox.addEventListener('change', () => {
        console.log('change','caption',$caption_checkbox.checked)
        $caption.classList.toggle('page-caption-show',$caption_checkbox.checked)
        api.settings_change({caption: $caption_checkbox.checked}).then(update_settings)
    })
    $footer_checkbox.addEventListener('change', () => {
        $footer.classList.toggle('page-footer-show',$footer_checkbox.checked)
        api.settings_change({footer: $footer_checkbox.checked}).then(update_settings)
    })
    $sidebar_close.addEventListener('click', () => {
        $sidebar.classList.remove('page-sidebar-show')
        api.settings_change({sidebar:false}).then(update_settings)
    })
    $sidebar_items.appendChild(login({api}))
    $sidebar_items.appendChild(logon({api}))
    $caption_checkbox.checked = true
    $footer_checkbox.checked = true

    api.on('login',async () => {
        api.settings().then(update_settings)
    })

    load()

    return $page

}

