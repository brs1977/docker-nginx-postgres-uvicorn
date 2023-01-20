export type Props = {}

export class ViewModel<T extends Props> {

    readonly props: Partial<T>
    private events = new Map<string,Set<Function>>();
    
    constructor(props?: T) {
        this.props = props ?? {}
    }

    protected setProps(props:Partial<T>) {
        let changed = false
        for (const key in props) {
            if (this.props[key] === props[key])
                continue
            changed = true
            this.props[key] = props[key]
            this.emit(`change:${key.toString()}`)
        }
        if (changed)
            this.emit('change')

    }

    protected getProp<K extends keyof T>(key:K) {
        return this.props[key]
    }

    on(event:string,callback:Function) {
        callback()
        const events = this.events
        let callbacks = events.get(event)
        if (!callbacks) {
            callbacks = new Set<Function>()
            events.set(event,callbacks)
        }
        callbacks.add(callback)
        return () => {
            const callbacks = events.get(event)
            if (!callbacks)
                return
            callbacks.delete(callback)
            if (callbacks.size == 0)
                events.delete(event)
        }
    }

    emit(event:string) {
        const callbacks = this.events.get(event)
        if (!callbacks)
            return
        callbacks.forEach(callback => callback())
    }
}