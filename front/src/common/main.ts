export function main() {
    const range = document.createRange()
    const fragment = range.createContextualFragment(`
        <div class="page">
            <div class="page__header header">
                <a href="#" class="icon icon--hamburger"></a>
                <div class="header__title">Заголовок</div>
            </div>
            <div class="page__caption caption">
                <div class="caption__title">Шапка</div>
                <a href="#" class="icon icon--close"></a>
            </div>
            <aside class="page__sidebar sidebar">
                <div class="sidebar__header">
                    <div class="sidebar__title">Боковая панель</div>
                    <a href="#" id="sidebar-close" class="icon icon--close"></a>
                </div>
                <div class="sidebar__content"></div>
                <div class="sidebar__footer">
                    <label>
                        Шапка
                        <input type="checkbox" value="yes">
                    </label>
                    <label>
                        Подвал
                        <input type="checkbox" value="yes">
                    </label>
                </div>
            </aside>
            <main class="page__workspace workspace">Рабочая область</main>
            <footer class="page__footer footer">
                <div class="footer__title">Подвал</div>
            </footer>
        </div>
    `)    // return h('main.main',
    //     header(),
    //     // sidebar(),
    //     // footer()
    // )
    const page = fragment.querySelector('.page')! as HTMLElement
    const header = page.querySelector('.page__header')! as HTMLElement
    const caption = page.querySelector('.page__caption')!  as HTMLElement
    const sidebar = page.querySelector('.page__sidebar')!  as HTMLElement
    const workspace = page.querySelector('.page__workspace')!  as HTMLElement
    const checkbox = Array.from(page.querySelectorAll('input[type=checkbox]')).map(cb => cb as HTMLInputElement)
    const footer = page.querySelector('.page__footer')! as HTMLElement
    page.addEventListener('mousemove', (e: MouseEvent) => {
        if (e.clientY > header.offsetHeight && e.clientY < header.offsetHeight + 20)
            caption.classList.add('page__caption--show')
        if (e.clientY > workspace.offsetTop && !checkbox[0].checked) 
            caption.classList.remove('page__caption--show')
        if (e.clientY > page.offsetHeight - 20) 
            footer.classList.add('page__footer--show')
        if (e.clientY < footer.offsetTop && !checkbox[1].checked) 
            footer.classList.remove('page__footer--show')
        if (e.clientX < 20 && e.clientY > caption.offsetTop + caption.offsetHeight) 
            sidebar.classList.add('page__sidebar--show')
        if (e.clientX > sidebar.offsetWidth + 10)
            sidebar.classList.remove('page__sidebar--show')
    })
    header.querySelector('.icon--hamburger')!.addEventListener('click',() => {
        const checked = sidebar.classList.contains('page__sidebar--show')
        sidebar.classList.toggle('page__sidebar--show',!checked)
    })
    caption.querySelector('.icon--close')!.addEventListener('click',e => {
        e.preventDefault()
        caption.classList.remove('page__caption--show')
        checkbox[0].checked = false
    })
    sidebar.querySelector('.icon--close')!.addEventListener('click',() => {
        const checked = sidebar.classList.contains('page__sidebar--show')
        sidebar.classList.toggle('page__sidebar--show',!checked)
    })
    checkbox.forEach(cb => {
        cb.addEventListener('change',()=> {
            if (cb === checkbox[0]) {
                caption.classList.toggle('page__caption--show',cb.checked)
            }
            else if (cb === checkbox[1]) {
                footer.classList.toggle('page__footer--show',cb.checked)
            }
        })
    })
    checkbox[0].checked = false
    checkbox[0].checked = false
    return fragment;
}