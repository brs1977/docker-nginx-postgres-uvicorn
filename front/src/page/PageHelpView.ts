import { View } from "./View"

export class PageHelpView extends View<HTMLDivElement> {
    constructor() {
        super(/*html*/`
        <div class="tabs help-tabs">
            <label class="tabs-expand"></label>
            <input class="tabs-input" type="radio" name="tabs" id="help-tab1" checked="checked">
            <label class="tabs-label" for="help-tab1">Справка</label>
            <div class="tabs-tab">
                <div class="help-item">1. Для начала работы необходимо авторизоваться(ввести логин и пароль)</div>
                <div class="help-item">2. Главное меню(Шапка) и дополнительная информация(Подвал) доступны в Боковой панели(см.выше)</div>
                <div class="help-item">3. Подробная контекстная помощь - правый верхний угол страницы</div>
            </div>
            <input class="tabs-input" type="radio" name="tabs" id="help-tab2">
            <label class="tabs-label" for="help-tab2">Инструменты</label>
            <div class="tabs-tab">
                <div class="accord">
                    <div class="accord-tab">
                        <input class="accord-input" type="checkbox" id="tools-tab1">
                        <label class="accord-label" for="tools-tab1">Входящие</label>
                        <div class="accord-data">
                            <ul class="accord-list">
                                <li class="accord-item"><img class="accord-icon" src="/data/node.svg"><span>Исходящие</span></li>
                                <li class="accord-item"><img class="accord-icon" src="/data/node.svg"><span>Избранное</span></li>
                                <li class="accord-item"><img class="accord-icon" src="/data/node.svg"><span>Недавние документы</span></li>
                            </ul>
                        </div>
                    </div>
                    <div class="accord-tab">
                        <input class="accord-input" type="checkbox" id="tools-tab2">
                        <label class="accord-label" for="tools-tab2">Общие папки</label>
                        <div class="accord-data">
                            <ul class="accord-list">
                                <li class="accord-item"><img class="accord-icon" src="/data/node.svg"><span>Договоры</span></li>
                                <li class="accord-item"><img class="accord-icon" src="/data/node.svg"><span>Компания</span></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `)
    }
}