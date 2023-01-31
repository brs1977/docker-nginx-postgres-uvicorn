import { PageViewModel } from "./PageViewModel";
import { View } from "./View";

/*
<div class="logon-short">Тут краткое описание (1-2 предложения) текущей страницы</div>
<div>
    <div class="logon-tabs">
        <div class="logon-tab logon-tab-active">Помощь</div>
        <div class="logon-tab">Инструменты</div>
</div>
<div class="logon-tabs-data">
    <ol class="logon-help logon-tab-data logon-tab-data-active">
        <li class="logon-help-item">Для начала работы необходимо авторизоваться(ввести логин и пароль)</li>
        <li class="logon-help-item">Главноне меню(Шапка) и дополнительная информация(Подвал) доступны в Боковой панели(см.выше)</li>
        <li class="logon-help-item">Подробная контекстная помощь - правый верхний угол страницы</li>
    </ol>
    <ul class="logon-tab-data logon-tree">
        <li class="logon-tree-group">
            <div class="logon-tree-node">Входящие</div>
            <ul class="logon-tree logon-tree-items">
                <li class="logon-tree-item"><img class="logon-icon" src="${node}"><span>Исходящие</span></li>
                <li class="logon-tree-item"><img class="logon-icon" src="${node}"><span>Избранное</span></li>
                <li class="logon-tree-item"><img class="logon-icon" src="${node}"><span>Недавние документы</span></li>
            </ul>
        <li>
        <li class="logon-tree-group">
            <div class="logon-tree-node">Общие папки</div>
            <ul class="logon-tree logon-tree-items">
                <li class="logon-tree-item"><img class="logon-icon" src="${node}"><span>Договоры</span></li>
                <li class="logon-tree-item"><img class="logon-icon" src="${node}"><span>Компания</span></li>
            </ul>
        </li>
    </ul>
</div>
*/

export class PageLogonView extends View<HTMLDivElement> {
    constructor(viewModel:PageViewModel) {
        super(/*html*/`
        <div class="logon">
            <hr class="logon-line">
            <div class="logon-header">
                <div class="logon-title">Навигация</div>
                <a href="#"><img class="logon-icon" src="/data/back.svg"></a>
                <a href="#"><img class="logon-icon" src="/data/forward.svg"></a>
                <a href="#"><img class="logon-icon" src="/data/down.svg"></a>
                <a href="#"><img class="logon-icon" src="/data/up.svg"></a>
            </div>
            <hr class="logon-line">
            <div class="logon-data">
                <div class="login-label">логин:</div>
                <div class="login-value" id="login-fio">значение</div>
                <div class="login-label">статус:</div>
                <div class="login-value" id="login-status">значение</div>
                <div class="login-label">в системе:</div>
                <div class="login-value" id="login-time">ЧЧ:ММ:CC</div>
            </div>
            <hr class="logon-line">
            <div class="logon-footer">
                <a href="#">Кабинет</a>
                <a href="#" id="logon-logout">Выйти</a>
            </div>
        </div>
        `)

        this.root.querySelector('#logon-logout')?.addEventListener('click', e => {
            e.preventDefault()
            viewModel.logout()
        })

        viewModel.on('change:page',() => {
            const user = viewModel.page?.sidebar.user
            this.root.querySelector('#login-fio')!.textContent = user?.username ?? ''
            this.root.querySelector('#login-status')!.textContent = user?.status ?? ''
            
        })

        let tm: number|undefined = undefined

        viewModel.on('login',() => {
            const begin = new Date()
            tm = setInterval(() => {
                const datetime = viewModel.page?.sidebar.user?.datetime ?? ''
                const date = new Date(datetime)
                const start = isNaN(+date) ? begin : date
                const time = new Date(Date.now() - start.getTime()).toLocaleTimeString()
                this.root.querySelector('#login-time')!.textContent = time
            },1000)
        })

        viewModel.on('logout',() => {
            clearInterval(tm)
        })

    }
}