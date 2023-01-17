import ham from '../img/ham.jpg'
import mess from '../img/mess.png'
import data from '../img/data.png'
import papka from '../img/papka.png'
import nastr from '../img/nastr.png'
import help2 from '../img/help2.png'
import shild from '../img/shild.png'
import close from '../img/close.svg'
import { make_fragment } from '../core/html'

export type PageProps = {
    sidebar?: Node,
    workspace?: Node,
}

export function page() {
    const page = make_fragment(
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

                    <div class="caption-menu-item caption-menu-active">Главная</div>
                    <div class="caption-menu-item">Ввод</div>
                    <div class="caption-menu-item">Аналитика</div>
                    <div class="caption-menu-item">Данные</div>
                    <div class="caption-menu-item">ОФАС</div>
                    <div class="caption-menu-item">Документы</div>
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
                <div class="div-work">
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

    const hamburger = page.querySelector<HTMLElement>('.header-hamburger')!
    const caption = page.querySelector<HTMLElement>('.page-caption')!
    const sidebar = page.querySelector<HTMLElement>('.page-sidebar')!
    const caption_checkbox = page.querySelector<HTMLInputElement>('.sidebar-checkbox input[name=caption]')!
    const footer_checkbox = page.querySelector<HTMLInputElement>('.sidebar-checkbox input[name=footer]')!
    const sidebar_close = page.querySelector<HTMLElement>('.sidebar-close')!
    const footer = page.querySelector<HTMLElement>('.page-footer')!
    hamburger.addEventListener('click', () => {
        sidebar.classList.add('page-sidebar-show')
    })
    caption_checkbox.addEventListener('change', () => {
        caption.classList.toggle('page-caption-show',caption_checkbox.checked)
    })
    footer_checkbox.addEventListener('change', () => {
        footer.classList.toggle('page-footer-show',footer_checkbox.checked)
    })
    sidebar_close.addEventListener('click', () => {
        sidebar.classList.remove('page-sidebar-show')
    })
    caption_checkbox.checked = true
    footer_checkbox.checked = true
    return page

}