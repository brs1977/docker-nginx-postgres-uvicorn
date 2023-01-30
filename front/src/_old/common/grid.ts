import { h, on } from "../_old/core/dom"
import { button, input, textarea } from "../_old/core/html"

export type Column = {
    name: string,
    title: string,
    type: 'string' | 'number' | 'text'
}

export type StringColumn = Column & {
    type: 'string'
}

export type NumberColumn = Column & {
    type: 'number'
}

export type TextColumn = Column & {
    type: 'text'
}

export type GridColumn = StringColumn | NumberColumn | TextColumn

export type GridColumns = Array<GridColumn>

export type GridValue = string|number|null

export type GridRecord = Record<string,GridValue>

export type GridRecords = Array<GridRecord>;

export type GridModel = {
    load(): Promise<GridRecords>,
    save(index:number,record:GridRecord):Promise<GridRecord>,
    remove(index:number,record:GridRecord):Promise<GridRecord>,
}

export type GridParams = {
    title: string,
    columns: GridColumns,
    model:GridModel
}

export function grid_model_array(initial:GridRecords=[]): GridModel {
    const data:GridRecords = [...initial]
    async function load() {
        return data
    }
    async function save(index:number,record:GridRecord) {
        if (index === -1)
            data.push(record)
        else
            data[index] = record
        return record
    }
    async function remove(index:number,record:GridRecord) {
        if (index !== -1)
            data.splice(index,1)
        return record
    }
    return {
        load,
        save,
        remove
    }
}

export function grid_model_local(name:string): GridModel {
    function loadData():GridRecords {
        const s = localStorage.getItem(name)
        const data =  s ? JSON.parse(s) : []
        return data
    }
    function saveData(data:GridRecords) {
        localStorage.setItem(name,JSON.stringify(data))
    }
    async function load() {
        return loadData()
    }
    async function save(index:number,record:GridRecord) {
        const data = loadData()
        if (index === -1)
            data.push(record)
        else
            data[index] = record
        saveData(data)
        return record
    }
    async function remove(index:number,record:GridRecord) {
        const data = loadData()
        if (index !== -1)
            data.splice(index,1)
        saveData(data)
        return record
    }
    return {
        load,
        save,
        remove
    }
}

export function grid({title,columns,model}:GridParams) {

    let tbody:HTMLTableSectionElement 
    let active_row: HTMLTableRowElement | undefined = undefined
    let records: GridRecords = []

    function column_to_th(col:GridColumn) {
        const th = h('th',col.title)
        return th
    }

    function grid_cell(record:GridRecord,col:GridColumn) {
        let el: HTMLInputElement | HTMLTextAreaElement
        if (col.type === 'number')
            el = input({className:'grid__number'})
        else if (col.type === 'string')
            el = input({className: 'grid__string'})
        else {
            el = textarea({className: 'grid__text',oninput: (e:Event) => {
                const el = e.target as HTMLTextAreaElement
                el.style.height = el.scrollHeight + "px"
            }})
            const x = requestAnimationFrame(() => {
                el.style.height = el.scrollHeight + "px"
                cancelAnimationFrame(x)
            })

        }
        el.value = record[col.name]?.toString() ?? ''
        on(el,'focus',() => {
            set_row(el.closest('tr') as HTMLTableRowElement)
        })
        on(el,'change',async () => {
            const index = records.indexOf(record)
            record[col.name] = el.value
            const new_record = await model.save(index,record)
            if (index === -1)
                records.push(new_record)
            else
                records[index] = new_record
        })
        return el
    }

    function grid_record(record:GridRecord) {
        const tr = h('tr') as HTMLTableRowElement
        const cells = columns.map(col => h('td',grid_cell(record,col)))
        tr.append(...cells)
        return tr
    }

    function add_row(e:Event) {
        e.preventDefault()
        const tr = grid_record({})
        tbody.insertBefore(tr,null)
        const el = tr.cells[0]?.firstElementChild as HTMLElement
        if (el)
            el.focus()
        //(tr.cells[0]?.firstChild? as HTMLElement).focus()
    }

    async function del_row(e:Event) {
        e.preventDefault()
        if (!active_row) return
        const index = Array.from(tbody.rows).indexOf(active_row)
        const record = records[index]
        if (!record) return
        if (!confirm('Delete record?')) return
        await model.remove(index,record)
        active_row.remove()
        if (index < tbody.rows.length)
            set_row(tbody.rows[index])
        else if (tbody.rows.length) 
            set_row(tbody.rows[index-1])
        else
            set_row(undefined)
    }

    function set_row(row?:HTMLTableRowElement) {
        active_row = row
        Array.from(tbody.rows).forEach(row => row.classList.toggle('grid__row--active',active_row == row))        
    }

    async function load() {
        records = await model.load()
        const rows = records.map(grid_record)
        tbody.replaceChildren(...rows)
    }

    const el = h('div.grid',
        h('div.grid__header',
            h('div.grid__title',title),
            button({className: 'grid__button',onclick: add_row},'Добавить'),
            button({className: 'grid__button',onclick: del_row},'Удалить'),
        ),
        h('table.grid__table',
            h('thead',
                h('tr.grid__headrow',
                    ...columns.map(column_to_th)
                )
            ),
            tbody = h('tbody') as HTMLTableSectionElement
        )
    )

    on(el,'load',load)

    load()

    return el
}