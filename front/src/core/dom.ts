export type Props = {
    id?: string,
    className?: string,
    onclick?: EventListener,
    onmouseout?: EventListener,
}

export type Child = string | Node

export type Children = Array<Child>

export function is_child(props?:Props|Child):props is Child {
    return typeof(props) === 'string' || props instanceof Node
}

export function is_props(props?:Props|Child): props is Props {
    return typeof(props) === 'object' && !is_child(props)
}

export function props_to_attr(prop:string) {
    switch(prop) {
        case 'className': return 'class'
        case 'htmlFor': return 'for'
        case 'readOnly': return 'readonly'
        case 'colSpan': return 'colspan'
        default: return prop
    }
}

export function set_prop<T extends HTMLElement,K extends keyof T>(el:T,key:K,value?:T[K]) {
    if (value === undefined)
        el.removeAttribute(props_to_attr(key.toString()))
    else
        el[key] = value
}

function child_to_node(child:Child) {
    return (typeof(child) === 'string') ? document.createTextNode(child) : child
}

export function h(tag:string,props?:Props|Child,...children:Children) {
    const [tagName,...classNames] = tag.split('.')
    const el = document.createElement(tagName)
    if (classNames.length)
        el.className = classNames.join(' ')
    if (is_props(props)) {
        set_prop(el,'id',props.id)
        if (props.className)
            el.className += (el.className ? ' ' : '') + props.className
        set_prop(el,'onclick',props.onclick)
        set_prop(el,'onmouseout',props.onmouseout)
    }
    if (is_child(props))
        children.unshift(props)
    const nodes = children.map(child_to_node)
    el.append(...nodes)
    return el 
}

export function fragment(...children:Children) {
    const frag = document.createDocumentFragment()
    const nodes = children.map(child_to_node)
    frag.append(...nodes)
    return frag
}

export function on(el:HTMLElement|Window|Document,event:string,listener:EventListener) {
    el.addEventListener(event,listener)
}

export function emit<T>(el:HTMLElement|null,event:string,detail?:T) {
    if (el)
        el.dispatchEvent(new CustomEvent<T>(event,{detail}))
}
