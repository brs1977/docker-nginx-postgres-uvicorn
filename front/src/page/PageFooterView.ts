import { View } from "./View";

export class PageFooterView extends View<HTMLDivElement> {
    constructor() {
        super(/*html*/`
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
        `)
    }
}