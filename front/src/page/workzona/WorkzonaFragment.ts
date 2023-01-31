import { PageViewModel } from "../PageViewModel";
import { createElement } from "../Utils";
import { Fragment } from "../View";

export class WorkzonaFragment extends Fragment {
    constructor(viewModel: PageViewModel) {
        super(/*html*/`
        <div class="div-work pic-m2"></div>
        <div class="workspace">
            <div>
                <img class="rz-shildik" src="/data/11_1_1_2.png" alt="Шильд">
            </div>   
            <div class="workspace-title">Администрирование информационного пространства Системы</div>
            <div class="workspace-data"> 
                <div class="workspace-tabs">
                    <div class="workspace-tab workspace-tab-first"></div>
                    <div class="workspace-tab workspace-tab-active">Режим</div>
                    <div class="workspace-tab">Настройки</div>
                    <div class="workspace-tab-expand"></div>
                </div>
                <div class="div-end-zag">
                     Управление разграничением доступа и безопасности информации
                </div>
            </div>
        </div>
        `)
        const background = this.root.querySelector<HTMLElement>('.pic-m2')!
        const title = this.root.querySelector<HTMLElement>('.workspace-title')!
        const shildik = this.root.querySelector<HTMLImageElement>('.rz-shildik')!
        const tabs = this.root.querySelector<HTMLElement>('.workspace-tabs')!
        const endTitle = this.root.querySelector<HTMLElement>('.div-end-zag')!
        viewModel.on('change:page',() => {
            const work_zona = viewModel.page?.work_zona
            if (work_zona?.background)
                background.style.backgroundImage = `url('/data/${work_zona.background}')`
            else
                background.style.removeProperty('background-image')
            title.textContent = work_zona?.title ?? ''
            title.classList.toggle('workspace-title-hide',!work_zona?.title)
            shildik.src = work_zona?.icon ? `/data/${work_zona.icon}` : ''
            shildik.classList.toggle('rz-shildik-hide',!work_zona?.icon)
            tabs.classList.toggle('workspace-tabs-hide',!work_zona?.tabs)
            tabs.querySelectorAll<HTMLElement>('.workspace-tab:not(:first-child)').forEach(it => it.remove())
            if (work_zona?.tabs) {
                work_zona.tabs.forEach(it => {
                    const el = createElement(/*html*/`<div class="workspace-tab">${it.name}</div>`)
                    el.classList.toggle('worspace-tab-active',!!it.active)
                    tabs.insertBefore(el,tabs.querySelector('.workspace-tab-expand'))
                })
            }
            endTitle.textContent = work_zona?.end_title ?? ''
            endTitle.classList.toggle('div-end-zag-hide',!work_zona?.end_title)
        })
    }
}