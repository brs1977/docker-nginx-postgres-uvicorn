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
import { API, is_alert_action, is_page_action, MenuItem } from '../api/api'
import { on } from '../core/dom'
import { make_page } from './pages'

export type PageProps = {
    api: API
}

function sort_menu (a:MenuItem,b:MenuItem) { return a.kod - b.kod }

function setup_actions(api:API,el:HTMLLinkElement,item:MenuItem) {
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
        console.log('page',item.kod)
        on(el,'click',async (e) => {
            e.preventDefault()
            const workspace = make_page(item.kod)
            el.closest('.page')?.querySelector<HTMLElement>('.workspace')?.replaceChildren(workspace)
        })
        //page({api,root,workspace,is_caption:$caption_checkbox.checked,is_footer:$footer_checkbox.checked})
    }
}

export function page({api}:PageProps) {
    async function load() {
        const menu = await api.menu()
        const nodes = menu
        .filter(item => item.parent === 0)
        .sort(sort_menu)
        .map((item,index) => {
            let el:HTMLElement
            const children = menu.filter(child => child.parent === item.kod)
            .sort(sort_menu)
            .map(child => {
                const el = make_element(/*html*/`
                    <li class="dropdown-item">
                        <a class="dropdown-link" href="#">${child.name}</a>
                    </li>
                `)
                setup_actions(api,el.querySelector<HTMLLinkElement>('.dropdown-link')!,child)
                return el
            })
            if (!children.length) {
                el = make_element(/*html*/`
                    <a href="#" class="caption-menu-item caption-menu-active">${item.name}</a>
                `)
                setup_actions(api,el as HTMLLinkElement,item)
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
            el.classList.toggle('caption-menu-active',index === 0)
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
                        <div class="div-gran0 block" style="height:96px">логин</div>
                        <div class="div-gran0 block" style="height:72px">помошь</div>
                        <div class="div-gran0 block" style="height:284px">панели</div>
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
    const $workspace = $page.querySelector<HTMLElement>('.page-workspace')!
    const $footer = $page.querySelector<HTMLElement>('.page-footer')!
    $hamburger.addEventListener('click', () => {
        $sidebar.classList.add('page-sidebar-show')
    })
    $caption_checkbox.addEventListener('change', () => {
        $caption.classList.toggle('page-caption-show',$caption_checkbox.checked)
    })
    $footer_checkbox.addEventListener('change', () => {
        $footer.classList.toggle('page-footer-show',$footer_checkbox.checked)
    })
    $sidebar_close.addEventListener('click', () => {
        $sidebar.classList.remove('page-sidebar-show')
    })
    $caption_checkbox.checked = false
    $footer_checkbox.checked = false
    
    load()

    return $page

}

