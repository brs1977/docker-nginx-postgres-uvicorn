export function main() {
    const range = document.createRange()
    const fragment = range.createContextualFragment(`
        <div class="page">
                <div class="header">
                    <a href="#" id="sidebar-open" class="icon icon--hamburger"></a>
                    <div class="header__title">Заголовок</div>
                </div>
                <div class="caption">
                    <div class="caption__title">Шапка</div>
                    <a href="#" id="caption-close" class="icon icon--close"></a>
                </div>
                <main class="main">
                    <aside id="sidebar" class="sidebar">
                        <div class="sidebar__header">
                            <div class="sidebar__title">Боковая панель</div>
                            <a href="#" id="sidebar-close" class="icon icon--close"></a>
                        </div>
                        <div class="sidebar__content"></div>
                        <div class="sidebar__footer">
                            <label>
                                Шапка
                                <input id="caption-checkbox" type="checkbox" checked>
                            </label>
                            <label>
                                Подвал
                                <input id="footer-checkbox" type="checkbox" checked>
                            </label>
                        </div>
                    </aside>
                    <div class="workspace">Рабочая область</div>
                </main>
                <footer id="footer" class="footer">
                    <div class="footer__title">Подвал</div>
                </footer>
            </div>`)    // return h('main.main',
    //     header(),
    //     // sidebar(),
    //     // footer()
    // )
    const sidebar = fragment.querySelector('#sidebar')!
    const caption = fragment.querySelector('.caption')!
    const captionCheckbox = fragment.querySelector('#caption-checkbox')! as HTMLInputElement
    const footerCheckbox = fragment.querySelector('#footer-checkbox')! as HTMLInputElement
    const footer = fragment.querySelector('footer')!
    fragment.querySelector('#caption-close')?.addEventListener('click', (e) => {
        e.preventDefault()
        caption.classList.add('caption--hide')
        captionCheckbox.checked = false
    })  
    sidebar.querySelector('#sidebar-close')!.addEventListener('click', (e) => {
        e.preventDefault()
        sidebar.classList.add('sidebar--hide')
    })
    fragment.getElementById('sidebar-open')!.addEventListener('click',(e) => {
        e.preventDefault()
        const hide = sidebar.classList.contains('sidebar--hide')                
        sidebar.classList.toggle('sidebar--hide',!hide)
    })
    captionCheckbox.addEventListener('click', () => {
        caption.classList.toggle('caption--hide',!captionCheckbox.checked)
    })
    footerCheckbox.addEventListener('click',() => {
        footer.classList.toggle('footer--hide',!footerCheckbox.checked)
    })
    return fragment;
}