import atten from '../img/atten.jpg'
import close_img from '../img/close.svg'
import { createElement } from "./Utils"

export type AlertProps = {
    title: string,
    text: string,
    buttons?: boolean
}

export async function showAlert(props:AlertProps) {
    const el = createElement(/*html*/`
        <div class="alert">
            <img class="alert-icon" src="${atten}">
            <div class="alert-data">
                <div class="alert-title">${props.title}</div>
                <div class="alert-message">${props.text}</div>
                <div class="alert-buttons">
                    <button class="alert-button" name="yes">Да</button>
                    <button class="alert-button" name="no">Нет</button>
                </div>
            </div>
            <img class="alert-close" src="${close_img}">
        </div>
    `)
    const {close} = showModal(el)
    el.querySelector<HTMLElement>('.alert-buttons')!.classList.toggle('alert-buttons-show',!!props.buttons)
    return new Promise<boolean>(resolve => {
        el.querySelector<HTMLElement>('.alert-close')?.addEventListener('click',() => {
            close()
            resolve(true)
        })
        el.querySelector<HTMLElement>('.alert-button[name=yes]')?.addEventListener('click', () => {
            close()
            resolve(true)
        })
        el.querySelector<HTMLElement>('.alert-button[name=no]')?.addEventListener('click', () => {
            close()
            resolve(false)
        })
    })
}

export function showModal(child:HTMLElement) {
    function close() {
        el.remove()
    }
    const el = createElement(/*html*/`<div class="modal">
        <div class="modal-inner"></div>
    </div>`)!
    el.querySelector('.modal-inner')!.appendChild(child)
    document.body.appendChild(el)
    return {
        close
    }
}