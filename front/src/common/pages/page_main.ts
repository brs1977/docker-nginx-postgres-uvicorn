import { make_fragment } from "../../core/html"
import i_11_1_1_1 from '../../img/11_1_1_1.png'
import i_11_1_1_2 from '../../img/11_1_1_2.png'
import i_32_1_1_4 from '../../img/32_1_1_4.png'
import i_11_1_1_3 from '../../img/11_1_1_3.png'
import i_33_6_1_1 from '../../img/33_6_1_1.png'
import i_33_4_1_3 from '../../img/33_4_1_3.png'
import i_33_8_1_2 from '../../img/33_8_1_2.png'

export function page_main() {
    return make_fragment(/*html*/`
        <div class="workspace-title">Система ситуационного анализа и прогнозирования состояния безопасности полетов воздушных судов авиации Вооруженных Сил Российской Федерации</div>
        <div class="workspace-data"> 
                        <!-- <div class="div-work"> -->
            <div class="gs-row-0  div-gran">
                <img class="gs-pic div-gran" src="${i_11_1_1_1}" alt="Шильдик ГЛАВНАЯ">
                <span class="gs-txt div-gran">Главная страница Системы (перечень модулей, личный кабинет пользовыателя, настройки)</span>
            </div>
    <!-- ПЕРВАЯ ПАРА *****************************************************************************************************************************************-->
            <div class="gs-row-0 div-gran">
                <div class="gs-row gs-row-49 div-gran">
                    <div class="proskok-row"></div>
                    <img class="gs-pic div-gran" src="${i_11_1_1_2}" alt="Шильдик ГЛАВНАЯ">
                    <span class="gs-txt div-gran">Модуль приема информации и информационного обмена</span>
                </div>
                <div class="gs-row gs-row-49  div-gran">
                    <img class="gs-pic div-gran" src=".${i_32_1_1_4}" alt="Шильдик ГЛАВНАЯ">
                    <span class="gs-txt div-gran">Модуль контроля и сопровождения базы данных Системы</span>
                </div>
            </div>
    <!-- ВТОРАЯ ПАРА *****************************************************************************************************************************************-->
            <div class="gs-row-0 div-gran">
                <div class="gs-row gs-row-49  div-gran">
                    <div class="proskok-row"></div>
                    <div class="proskok-row"></div>
                    <img class="gs-pic div-gran" src="${i_11_1_1_3}" alt="Шильдик ГЛАВНАЯ">
                    <span class="gs-txt div-gran">Модуль ситуационного анализа и прогнозирования</span>
                </div>
                <div class="gs-row gs-row-49  div-gran">
                    <div class="proskok-row"></div>
                    <img class="gs-pic div-gran" src="${i_33_6_1_1}" alt="Шильдик ГЛАВНАЯ">
                    <span class="gs-txt div-gran">Модуль надзорной деятельности (модуль 1-й инспекции)</span>
                </div> 
            </div>
    <!-- ТРЕТЬЯ ПАРА *****************************************************************************************************************************************-->
            <div class="gs-row-0 div-gran">
                <div class="proskok-row"></div>
                <div class="proskok-row"></div>
                <div class="proskok-row"></div>
                <div class="gs-row gs-row-49 div-gran">
                    <img class="gs-pic div-gran" src="${i_33_4_1_3}" alt="Шильдик ГЛАВНАЯ">
                <span class="gs-txt div-gran">Документы (формирование отчетов, оперативных донесений, подготовка обзорных материалов по теме)</span>
                </div>
                <div class="gs-row gs-row-49 div-gran">
                    
                    <img class="gs-pic div-gran" src="${i_33_8_1_2}" alt="Шильдик ГЛАВНАЯ">
                    <span class="gs-txt div-gran">Модуль ОФАС (модуль 2-й инспекции)</span>
                </div>
            </div>
        </div>
    `)                           
}