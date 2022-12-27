import { fragment, h, on } from "../core/dom"
import { button, field_id, form, input, label, modal, textarea } from "../core/html"

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

export type EditParams = {
    record: GridRecord,
    columns: GridColumns,
    onsave: (record:GridRecord) => Promise<void>
}

function column_to_field(record:GridRecord,col:GridColumn) {
    let ctrl: HTMLInputElement | HTMLTextAreaElement
    const value = record[col.name]?.toString() ?? ''
    const id = field_id()
    if (col.type === 'number')
        ctrl = input({id,value})
    else if (col.type === 'string')
        ctrl = input({id,value})
    else
        ctrl = textarea({id,value})
    on(ctrl,'change',() => {
        record[col.name] = ctrl.value
    })
    return fragment(
        label({htmlFor: id},col.title),
        ctrl
    )
}

export function edit({record,columns,onsave}: EditParams) {

    async function onsubmit(e:Event)  {
        e.preventDefault()
        for (const name in form_record) {
            record[name] = form_record[name]
        }
        await onsave(record)
        close()
    }

    function cancel(e:Event) {
        e.preventDefault()
        close()
    }

    const form_record = {...record}

    const el = form({onsubmit,className:'form'},
        h('div.form__fields',...columns.map(col => column_to_field(form_record,col))),
        h('div.form__buttons',
            button({type:'submit'},'Сохранить'),
            button({onclick: cancel},'Отмена')
        )
    )
    const {close} = modal(el)
    if (el[0] instanceof HTMLElement)
        el[0].focus()
}

export function grid({title,columns,model}:GridParams) {

    let tbody:HTMLTableSectionElement 
    let active_row: HTMLTableRowElement | undefined = undefined
    let records: GridRecords = []

    function column_to_th(col:GridColumn) {
        const th = h('th',col.title)
        return th
    }

    function grid_record(record:GridRecord) {
        async function onsave(record:GridRecord) {
            const index = records.indexOf(record)
            records[index] = await model.save(index,record)
            columns.forEach((col,index) => {
                tr.cells[index].textContent = record[col.name]?.toString() ?? ''
            })
        }
        const tr = h('tr') as HTMLTableRowElement
        const cells = columns.map(col => h('td',record[col.name]?.toString() ?? ''))
        tr.append(...cells)
        on(tr,'click', (e) => {
            e.preventDefault()
            set_row(tr)
        })
        on(tr,'dblclick',(e) => {
            e.preventDefault()
            edit({record,columns,onsave})
        })
        return tr
    }

    function add_row(e:Event) {
        async function onsave(record:GridRecord) {
            record = await model.save(-1,record)
            records.push(record)
            const tr = grid_record(record)
            tbody.appendChild(tr)
            set_row(tr)
        }
        e.preventDefault()
        const record = {}
        edit({record,columns,onsave})
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

