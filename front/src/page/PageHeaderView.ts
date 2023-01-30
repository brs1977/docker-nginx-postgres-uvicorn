import { PageViewModel } from "./PageViewModel";
import { createElement } from "./Utils";
import { View } from "./View";

// <div> <img class="shildik-own" src="/data/mess.png" alt="Сообщения"> </div>
// <div> <img class="shildik-own" src="/data/data.png" alt="Ввод данных"> </div>
// <div> <img class="shildik-own" src="/data/papka.png" alt="Документы"> </div>
// <div> <img class="shildik-own" src="/data/nastr.png" alt="Настройки"> </div>
// <div> <img class="shildik-own" src="/data/help2.png" alt="Помощь"> </div>
// <div class="shildik-own">
//     <img class="shildik-own" src="/data/shild.png" alt="Шильдик методологии">
// </div>

export class PageHeaderView extends View<HTMLDivElement> {
    constructor(readonly viewModel:PageViewModel) {
        super(/*html*/`            
            <div class="header">
                <img class="header-hamburger" src="/data/ham.jpg">
                <span class="header-title">Служба безопасности полетов авиации Вооруженных сил Российской Федерации</span>
            </div>
        `)
        viewModel.on('change:page',() => {
            const {icons=[],title=''} = viewModel.page?.verh ?? {}
            this.root.querySelector('.header-title')!.textContent = title
            const children = icons.map(icon => createElement(`<img class="shildik-own" src="/data/${icon}">`))
            this.root.querySelector('.header-icons')?.replaceChildren(...children)
            this.root.querySelectorAll('.shildik-own').forEach(it => it.remove())
            this.root.append(...children)
        })
        this.root.querySelector<HTMLElement>('.header-hamburger')!.addEventListener('click', e => {
            e.preventDefault()
            viewModel.changeSettings({sidebar:true})
        })
    }
}