import { Child, Children, h, is_props, Props, set_prop } from "./dom";

export type ButtonProps = Props & {
    type?: 'button' | 'submit' | 'reset',
    //onclick?: EventListener
}

export function button(props:ButtonProps|Child,...children:Children) {
    const el = h('button',props,...children) as HTMLButtonElement
    if (is_props(props)) {
        set_prop(el,'type',props.type)
        //set_prop(el,'onclick',props.onclick)
    }
    return el
}

export type TDProps = Props & {
    colspan?: number
}

export function td(props:TDProps|Child,...children:Children) {
    const el = h('td',props,...children) as HTMLTableCellElement
    if (is_props(props)) {
        set_prop(el,'colSpan',props.colspan)
    }
    return el
}

export type LabelProps = Props & {
    htmlFor?: string
}

export function label(props?:LabelProps|Child,...children:Children) {
    const el =  h('label',props,...children) as HTMLLabelElement
    if (is_props(props))
        set_prop(el,'htmlFor',props.htmlFor)
    return el
}

export type InputProps = Props & {
    name?: string,
    checked?: boolean
    type?: string,
    accept?: string,
    value?: string,
    autofocus?: boolean,
}

export function input(props?:InputProps|Child,...children:Children) {
    const el = h('input',props,...children) as HTMLInputElement
    if (is_props(props)) {
        set_prop(el,'type',props.type)
        set_prop(el,'name',props.name)
        set_prop(el,'accept',props.accept)
        set_prop(el,'value',props.value)
        set_prop(el,'autofocus',props.autofocus)
        set_prop(el,'checked',props.checked)
    }
    return el
}

export type TextAreaProps = Props & {
    rows?: number,
    oninput?: EventListener,
    value?: string,
    autofocus?: boolean,
}

export function textarea(props?:TextAreaProps|Child,...children:Children) {
    const el = h('textarea',props,...children) as HTMLTextAreaElement
    if (is_props(props)) {
        set_prop(el,'rows',props.rows)
        set_prop(el,'oninput',props.oninput)
        set_prop(el,'value',props.value)
        set_prop(el,'autofocus',props.autofocus)
    }
    return el
}

export type FormProps = Props & {
    onsubmit?: EventListener
}

export function form(props?:FormProps|Child,...children:Children) {
    const el = h('form',props,...children) as HTMLFormElement
    if (is_props(props)) {
        set_prop(el,'onsubmit',props.onsubmit)
    }
    
    return el
}

let FIELD_ID = 0

export function field_id() {
    return `field-${++FIELD_ID}`
}

export function modal(child:HTMLElement) {
    function close() {
        el.remove()
    }
    const el = h('div.modal',
        h('div.modal__inner',child)
    )
    document.body.appendChild(el)
    return {
        close
    }
}

export type LinkProps = Props & {
    href?: string,
    //onclick?: EventListener
}

export function link(props?:LinkProps | Child,...children: Children) {
    const el = h('a',props,...children) as HTMLLinkElement
    if (is_props(props)) {
        set_prop(el,'href',props.href)
        //set_prop(el,'onclick',props.onclick)
    }
    return el
}

export type ImgProps = Props & {
    src?: string
}

export function img(props?:ImgProps | Child,...children: Children) {
    const el = h('img',props,...children) as HTMLImageElement
    if (is_props(props)) {
        set_prop(el,'src',props.src)
    }
    return el
}

export function make_fragment(html:string) {
    const r = document.createRange()
    return r.createContextualFragment(html)
}

export function make_element<T extends HTMLElement>(html:string) {
    const r = document.createRange()
    const f = r.createContextualFragment(html)
    return f.firstElementChild as T
}



