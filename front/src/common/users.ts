import { API } from "../api/api"
import { h } from "../core/dom"
import { button, td } from "../core/html"

type UsersParams = {
    api: API
}

export function users({api}:UsersParams) {
    async function load() {
        const button = el.querySelector('button')!
        button.disabled = true
        button.classList.add('refresh__button--refreshing')
        try {
            const users = await api.users()
            const rows = users.map(user => {
                return h('tr',
                    h('td','' + user.id),
                    h('td',user.name)
                )
            })
            el.querySelector('tbody')!.replaceChildren(...rows)
            el.querySelector('.refresh__label')!.textContent = `Последнее обновление: ${new Date().toLocaleString()}`
        } finally {
            button.classList.remove('refresh__button--refreshing')
            button.disabled = false
        }
    }
    async function onclick(e:Event) {
        e.preventDefault()
        load()
    }
    const el = h('div.table-view',
        h('h1','Пользователи'),
        h('table.content-table',
            h('thead',
                h('tr',
                    td('№'),
                    td('Имя')
                )
            ),
            h('tbody',
                h('tr',
                    td({colspan:2},'Загрузка данных...')
                )
        )
        ),
        h('div.refresh',
            h('span.refresh__label','Последнее обновление: никогда'),
            button({className:'refresh__button',type:'button',onclick})
        )
    )
    load()
    return el
}