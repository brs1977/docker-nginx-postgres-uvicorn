import { API } from "../api/api"
import { emit } from "../core/dom"
import { FailError } from "../core/utils"
import { toast } from './toast'
import { users } from "./users"

export type AppParams = {
    root: HTMLElement,
    api: API
}

export function app({api,root}:AppParams) {

    const $toast = toast()
 
    window.addEventListener('unhandledrejection', e => {
        console.log(e)
        const message = (e.reason instanceof FailError) ? e.reason.message : `Ошибка: ${e.reason.message}`
        emit($toast,'show',message)
    })

    const $users = users({api})
    root.appendChild($users)

}