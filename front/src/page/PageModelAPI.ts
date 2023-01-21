import { createSettings, Menu, PageModel, API, Settings, User, WorkspaceMainProps } from "./PageTypes";

export class PageModelAPI implements PageModel {

    static SETTINGS = 'SETTINGS'
    private settings = createSettings()
    private isLoggedIn = false

    constructor(readonly api: API) { }

    async loadMenu(): Promise<Menu> {
        return this.api.get<Menu>('config/menu');
    }

    async loadSettings(): Promise<Settings> {
        if (!this.isLoggedIn)
            return this.settings
        let settings = createSettings()
        try {
            const s = localStorage.getItem(PageModelAPI.SETTINGS)
            if (s) {
                const obj = JSON.parse(s)
                if (typeof (obj) === 'object')
                    settings = { ...settings, ...obj }
            }
        } catch (e) {
            console.log('loadSettings', e)
        }
        return settings
    }

    async login(username: string, password: string) {
        await this.api.login(username, password)
        this.isLoggedIn = true
    }

    async loadUser(): Promise<User> {
        return this.api.get<User>('users/me')
    }

    async saveSettings(settings: Settings): Promise<Settings> {
        if (this.isLoggedIn)
            localStorage.setItem(PageModelAPI.SETTINGS, JSON.stringify(settings))
        else
            this.settings = settings
        return settings
    }

    async logout() {
        await this.api.logout()
    }

    async loadWorkspace(kod: number) {
        //return await this.api.get<WorkspaceProps>(`config/menu/${kod}/`)
        const props: WorkspaceMainProps = { 
            kod, 
            type: 1, 
            title: 'Система ситуационного анализа и прогнозирования состояния безопасности полетов воздушных судов авиации Вооруженных Сил Российской Федерации',
            pic: "main.jpg", 
            picpic: 0, 
            n_par: [1, 2, 2, 2], 
            m_par: [{ 
                pic: "11_1_1_1.jpg", txt: "Главная страница Системы (перечень модулей, личный кабинет пользовыателя, настройки)" }, { pic: "111_1_1_4.jpg", txt: "Модуль приема информации и информационного обмена" }, { pic: "111_1_1_2.jpg", txt: "Модуль контроля и сопровождения базы данных Системы" }, { pic: "111_1_1_3.jpg", txt: "Модуль ситуационного анализа и прогнозирования" }, { pic: "133_6_1_1.jpg", txt: "Модуль надзорной деятельности (модуль 1-й инспекции)" }, { pic: "133_4_1_3.jpg", txt: "Документы (формирование отчетов, оперативных донесений, подготовка обзорных материалов по теме)" }, { pic: "133_8_1_2.jpg", txt: "Модуль ОФАС (модуль 2-й инспекции)" }] }
        return props
    }


} 