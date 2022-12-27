import { Child, Children, h, is_props, Props, set_prop } from "./dom";

export type ButtonProps = Props & {
    type?: 'button' | 'submit' | 'reset',
    onclick?: EventListener
}

export function button(props:ButtonProps|Child,...children:Children) {
    const el = h('button',props,...children) as HTMLButtonElement
    if (is_props(props)) {
        set_prop(el,'type',props.type)
        set_prop(el,'onclick',props.onclick)
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

export type InputProps = Props & {
    type?: string,
    accept?: string,
}

export function input(props?:InputProps|Child,...children:Children) {
    const el = h('input',props,...children) as HTMLInputElement
    if (is_props(props)) {
        set_prop(el,'type',props.type)
        set_prop(el,'accept',props.accept)
    }
    return el
}

export type TextAreaProps = Props & {
    rows?: number,
    oninput?: EventListener
}

export function textarea(props?:TextAreaProps|Child,...children:Children) {
    const el = h('textarea',props,...children) as HTMLTextAreaElement
    if (is_props(props)) {
        set_prop(el,'rows',props.rows)
        set_prop(el,'oninput',props.oninput)
    }
    return el
}