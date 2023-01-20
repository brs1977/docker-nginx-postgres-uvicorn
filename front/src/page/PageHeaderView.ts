import { PageViewModel } from "./PageViewModel";
import { View } from "./View";

import ham from '../img/ham.jpg'
import mess from '../img/mess.png'
import data from '../img/data.png'
import papka from '../img/papka.png'
import nastr from '../img/nastr.png'
import help2 from '../img/help2.png'
import shild from '../img/shild.png'

export class PageHeaderView extends View<HTMLDivElement> {
    constructor(readonly viewModel:PageViewModel) {
        super(/*html*/`            
            <div class="header">
                <img class="header-hamburger" src="${ham}">
                <span class="header-title">Служба безопасности полетов авиации Вооруженных сил Российской Федерации</span>
                <div> <img class="shildik-own" src="${mess}" alt="Сообщения"> </div>
                <div> <img class="shildik-own" src="${data}" alt="Ввод данных"> </div>
                <div> <img class="shildik-own" src="${papka}" alt="Документы"> </div>
                <div> <img class="shildik-own" src="${nastr}" alt="Настройки"> </div>
                <div> <img class="shildik-own" src="${help2}" alt="Помощь"> </div>
                <div class="shildik-own">
                    <img class="shildik-own" src="${shild}" alt="Шильдик методологии">
                </div>
            </div>
        `)
        this.root.querySelector<HTMLElement>('.header-hamburger')!.addEventListener('click', e => {
            e.preventDefault()
            viewModel.changeSettings({sidebar:true})
        })
    }
}