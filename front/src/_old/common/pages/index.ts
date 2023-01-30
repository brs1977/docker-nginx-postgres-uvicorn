import { fail } from "../../_old/core/utils";
import { page_main } from "./page_main";
import { page_test } from "./page_test";

const PAGES: Record<number,Function> =  {
    1: page_main,
    10: page_test
}

export function make_page(kod: number) {
    const func = PAGES[kod]
    const el = func()
    if (el === undefined)
        fail(`Страницы ${kod} не существует`)
    return el
}