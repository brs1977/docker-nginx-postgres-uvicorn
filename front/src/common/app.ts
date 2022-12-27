import { API } from "../api/api"
import { emit, on } from "../core/dom"
import { input } from "../core/html"
import { FailError } from "../core/utils"
import { grid, grid_model_local } from "./grid2"
import { toast } from './toast'
//import { users } from "./users"

export type AppParams = {
    root: HTMLElement,
    api: API
}

export function app({root}:AppParams) {

    const $toast = toast()
 
    window.addEventListener('unhandledrejection', e => {
        console.log(e)
        const message = (e.reason instanceof FailError) ? e.reason.message : `Ошибка: ${e.reason.message}`
        emit($toast,'show',message)
    })

    // const $users = users({api})
    // root.appendChild($users)


    const $upload = input({type:'file',accept:'application/json'})
    on($upload,'change',async () => {
        const file = $upload.files![0]
        if (!file) return
        const s = await file.text()
        localStorage.setItem('USERS',s)
        emit($grid,'load')
    })
    root.appendChild($upload)

    const $grid = grid({
        title: 'Пользователи',
        columns: [
            { name: 'id', title: '№', type: 'number'},
            { name: 'name', title: 'Имя', type: 'string'},
            { name: 'comments', title: 'Коментарий', type: 'text'},
        ],
        model : grid_model_local('USERS')
    })

    root.appendChild($grid)

}