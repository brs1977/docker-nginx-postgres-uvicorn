import { PageViewModel } from "./PageViewModel";
import { View } from "./View";

export class PageLoginView extends View<HTMLFormElement> {
    
    constructor(readonly viewModel:PageViewModel) {
        super(/*html*/`
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
                <button class="login-button" type="submit">ОК</button>
            </div>
        </form>
        `)

        this.root.addEventListener('submit', e => {
            e.preventDefault()
            const username = this.root.querySelector<HTMLInputElement>('input[name=username]')!.value
            const password = this.root.querySelector<HTMLInputElement>('input[name=password]')!.value
            viewModel.login(username,password)
        })
    }
}