import { make_fragment } from "../../core/html";

export function page_test() {
    return make_fragment(/*html*/`
        <div class="workspace-title">Заголовок</div>
        <div class="workspace-data">Рабочая область</div>
    `)
}