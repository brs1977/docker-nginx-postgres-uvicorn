interface CustomEventMap {
  "show": CustomEvent<string>
}

declare global {
  interface HTMLDivElement { //adds definition to Document, but you can do the same with HTMLElement
      addEventListener<K extends keyof CustomEventMap>(type: K,
          listener: (this: Document, ev: CustomEventMap[K]) => void): void;
  }
}

export function toast() {

  const el = document.createElement('div')
  el.className = 'toast'

  let hideTimeout: number | null = null

  document.body.append(el)

  function hide() {
      if (hideTimeout)
          clearTimeout(hideTimeout)
      el.classList.remove("toast-visible")
      document.removeEventListener('click', hide)
  }

  function show(message:string) {
      if (hideTimeout)
          clearTimeout(hideTimeout)

      el.textContent = message
      el.className = "toast toast-error toast-visible"

      // if (state) {
      //     el.classList.add(`toast--${state}`)
      // }

      hideTimeout = setTimeout(hide, 3000)

      document.addEventListener('click', hide)
  }

  el.addEventListener('show',(e:CustomEvent<string>) => show(e.detail))

  return el
}
