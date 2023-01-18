import { on } from "./dom"
import { make_fragment, modal } from "./html"
import atten from '../img/atten.jpg'
import close_img from '../img/close.svg'

export type AlertProps = {
    title: string,
    message: string,
    buttons?: boolean
}

export async function show_alert(props:AlertProps) {
    const f = make_fragment(/*html*/`
        <div class="alert">
            <img class="alert-icon" src="${atten}">
            <div class="alert-data">
                <div class="alert-title">${props.title}</div>
                <div class="alert-message">${props.message}</div>
                <div class="alert-buttons">
                    <button class="alert-button" name="yes">Да</button>
                    <button class="alert-button" name="no">Нет</button>
                </div>
            </div>
            <img class="alert-close" src="${close_img}">
        </div>
    `)
    const el = f.querySelector<HTMLElement>('.alert')!
    const {close} = modal(el)
    el.querySelector<HTMLElement>('.alert-buttons')!.classList.toggle('alert-buttons-show',!!props.buttons)
    return new Promise<boolean>(resolve => {
        on(el.querySelector<HTMLElement>('.alert-close')!,'click',() => {
            close()
            resolve(true)
        })
        on(el.querySelector<HTMLElement>('.alert-button[name=yes]')!,'click', () => {
            close()
            resolve(true)
        })
        on(el.querySelector<HTMLElement>('.alert-button[name=no]')!,'click', () => {
            close()
            resolve(false)
        })
    })
}