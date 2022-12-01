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