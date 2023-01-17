import i11_1_1_1 from '../img/11_1_1_1.png'
import i11_1_1_2 from '../img/11_1_1_2.png'
import i11_1_1_3 from '../img/11_1_1_3.png'
import i32_1_1_4 from '../img/32_1_1_4.png'
import i33_6_1_1 from '../img/33_6_1_1.png'
import i33_8_1_2 from '../img/33_8_1_2.png'
import i33_4_1_3 from '../img/33_4_1_3.png'
import { make_fragment } from '../core/html'

export function login() {
    return make_fragment(/*html*/`
      <form class="login">
        <div class="login-header">
          <a href="#">регистрация</a>
          <span>|</span>
          <a class="login-forgot" href="#">забыли пароль?</a>
        </div>
        <div class="login-data">
          <div class="login-title">Вход</div>
            <input class="login-input">
            <input class="login-input" type="password">
            <button class="login-button">ОК</button>
        </div>
      </form>
    `)
}

export function workspace() {
    return make_fragment(
      /*html*/`
      <div class="workspace-title">Система ситуационного анализа и прогнозирования состояния безопасности полетов воздушных судов авиации Вооруженных Сил Российской Федерации</div>
                                      
      <div class="workspace-data"> 
        <div class="gs-row-0 div-gran">
            <img class="gs-pic div-gran" src="${i11_1_1_1}" alt="Шильдик ГЛАВНАЯ">
            <span class="gs-txt div-gran">Главная страница Системы (перечень модулей, личный кабинет пользовыателя, настройки)</span>
        </div>
        <div class="gs-row-0 div-gran">
            <div class="gs-row gs-row-49 div-gran">
                <div class="proskok-row"></div>
                <img class="gs-pic div-gran" src="${i11_1_1_2}" alt="Шильдик ГЛАВНАЯ">
                <span class="gs-txt div-gran">Модуль приема информации и информационного обмена</span>
            </div>
            <div class="gs-row gs-row-49 div-gran">
                <div class="proskok-row"></div>
                <div class="proskok-row"></div>
                <img class="gs-pic div-gran" src="${i11_1_1_3}" alt="Шильдик ГЛАВНАЯ">
                <span class="gs-txt div-gran">Модуль ситуационного анализа и прогнозирования</span>
            </div>
        </div>
        <div class="gs-row-0 div-gran">
            <div class="proskok-row"></div>
            <div class="proskok-row"></div>
            <img class="gs-pic div-gran" src="${i32_1_1_4}" alt="Шильдик ГЛАВНАЯ">
            <span class="gs-txt div-gran">Модуль контроля и сопровождения базы данных Системы</span>
        </div>
        <div class="gs-row-0 div-gran">
            <div class="proskok-row"></div>
            <div class="proskok-row"></div>
            <div class="proskok-row"></div>
            <div class="gs-row gs-row-49 div-gran">
                <img class="gs-pic div-gran" src="${i33_6_1_1}" alt="Шильдик ГЛАВНАЯ">
                <span class="gs-txt div-gran">Модуль надзорной деятельности (модуль 1-й инспекции)</span>
            </div>
            <div class="gs-row gs-row-49 div-gran">
                <div class="proskok-row"></div>
                <div class="proskok-row"></div>
                <img class="gs-pic div-gran" src="${i33_8_1_2}" alt="Шильдик ГЛАВНАЯ">
                <span class="gs-txt div-gran">Модуль ОФАС (модуль 2-й инспекции)</span>
            </div>
        </div>

        <div class="gs-row-0 div-gran">
            <div class="proskok-row"></div>
            <div class="proskok-row"></div>
            <div class="proskok-row"></div>
            <div class="proskok-row"></div>
            <img class="gs-pic div-gran" src="${i33_4_1_3}" alt="Шильдик ГЛАВНАЯ">
            <span class="gs-txt div-gran">Документы (формирование отчетов, оперативных донесений, подготовка обзорных материалов по теме)</span>
        </div>   
      </div>
    `
    )
}
export function main() {

}