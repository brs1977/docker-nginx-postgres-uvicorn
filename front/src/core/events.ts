type Events = {
    on(event:string,callback:Function):Function
    emit(event:string):void
}
export function events(): Events {

    const callbacks = new Map<string,Set<Function>>()
    
    function on(event:string,callback:Function):Function {
        const _callbacks = callbacks.get(event) ?? new Set<Function>()
        callbacks.set(event,_callbacks)
        _callbacks.add(callback)
        return () => {
            _callbacks.delete(callback)
            if (!_callbacks.size)
                callbacks.delete(event)
        }
    }

    function emit(event:string) {
        const _callbacks = callbacks.get(event)
        if (_callbacks === undefined)
            return
        _callbacks.forEach(callback => callback())
    }

    return {
        on,
        emit
    }
}