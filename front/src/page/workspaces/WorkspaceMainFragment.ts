import { Fragment } from "../View";
import { WorkspaceMainViewModel } from "./WorkspaceMainViewModel";
import { createFragment } from "../Utils";

type Item = { pic: string, txt: string }
type ItemInfo = { type: 10 | 21 | 22, level: number }

export class WorkspaceMainFragment extends Fragment {
    constructor(viewModel: WorkspaceMainViewModel) {
        super(/*html*/`
        <img class="rz-shildik" alt="Шильдик типа">
        <div class="workspace-title"></div>
        <div class="workspace-data"></div>
        `)
        viewModel.on('change', () => {
            this.root.querySelector('.workspace-title')!.textContent = viewModel.title ?? ''
            const picpic = this.root.querySelector<HTMLImageElement>('.rz-shildik')!
            if (viewModel.picpic)
                picpic.src = this.getSrc(viewModel.picpic)
            picpic.classList.toggle('picpic-hide', !viewModel.picpic)
            const info: Array<ItemInfo> = []
            viewModel.n_par.forEach((it, index) => {
                if (it <= 1) {
                    info.push({ type: 10, level: index })
                } else {
                    info.push({ type: 21, level: index })
                    info.push({ type: 22, level: index })
                }
            })
            // const children = viewModel.m_par
            //     .map((m_par, index) => this.renderItem(m_par, info[index]))
            //     .map(it => createElement(it))
            const html = viewModel.m_par.map((m_par, index) => this.renderItem(m_par, info[index]))
                .join('')
            const f = createFragment(html)
            this.root.querySelector('.workspace-data')?.replaceChildren(f)
        })
    }

    renderItem(item: Item, info: ItemInfo) {
        switch (info.type) {
            case 10: return this.renderItem10(item, info)
            case 21: return this.renderItem21(item, info)
            case 22: return this.renderItem22(item, info)
        }
    }

    getProksok(info: ItemInfo) {
        return Array(info.level).fill(/*html*/`<div class="proskok-row"></div>`).join('')
    }

    getSrc(pic:string) {
        const src = `../img/${pic}`
        return new URL(src,import.meta.url).href
    }

    renderItem10(item: Item, info: ItemInfo) {
        const proskok = this.getProksok(info)
        const src = this.getSrc(item.pic)
        return /*html*/`
            <div class="gs-row-0 div-gran">
            ${proskok}
            <img class="gs-pic div-gran" src="${src}" alt="Шильдик ГЛАВНАЯ">
            <span class="gs-txt div-gran">${item.txt}</span>
        </div>`
    }

    renderItem21(item: Item, info: ItemInfo) {
        const proskok = this.getProksok(info)
        const src = this.getSrc(item.pic)
        return /*html*/`
        <div class="gs-row-0  div-gran">
            <div class="gs-row gs-row-49 div-gran">
                ${proskok}
                <img class="gs-pic div-gran" src="${src}" alt="Шильдик ГЛАВНАЯ">
                <span class="gs-txt div-gran">${item.txt}</span>
            </div>
        `
    }

    renderItem22(item: Item, _: ItemInfo) {
        const src = this.getSrc(item.pic)
        return /*html*/`
            <div class="gs-row gs-row-49  div-gran">
                <img class="gs-pic div-gran" src="${src}" alt="Шильдик ГЛАВНАЯ">
                <span class="gs-txt div-gran">${item.txt}</span>
            </div>
        </div>`        
    }
}