from fastapi import Request, Path, APIRouter, status, HTTPException, Depends
from app.api.v1.config.utils import read_config
from app.schemas.users import UserDB
from app.schemas import page
from app.api import security
from datetime import datetime
from abc import abstractmethod
from loguru import logger
from enum import Enum, EnumMeta
import os

config_doc = read_config()
router = APIRouter()

ROLE_STATUS_MAP = {
    1: "Гость",
    2: "Оператор",
    3: "Функционер",
    4: "Администратор",
}


class EnumMetaValue(EnumMeta):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.value
        return value


class Names(Enum, metaclass=EnumMetaValue):
    DESIGN = "design"
    USER = "user"
    VERH = "verh"
    HEAD = "head"
    SIDEBAR = "sidebar"
    WORK_ZONA = "work_zona"
    FOOTER = "footer"
    TITLE = "title"
    TITLES = "titles"
    BACKGROUND = "background"
    ICONS = "icons"
    ICON = "icon"
    ORGSTR = "orgstr"
    BROD = "brod"
    INS = "ins"
    ACTIVE_MENU = "active_menu"
    MENU = "menu"
    MENU_TYPE = "menu_typ"
    ALERT = "alert"
    REF = "ref"
    SUB = "sub"
    PAGE = "page"
    KOD = "kod"
    PATH_IMAGES = "path_images"
    MAS_TITLES = "mas_titles"
    MAS_ALERT = "mas_alert"
    ROLE_ID = "role_id"
    USERNAME = "username"
    DATETIME = "datetime"
    STATUS = "status"
    START_TITLE = 'start_title'
    CHECKBOX = 'checkbox'
    GRAPH_PAGE = 'graph_page'
    PAGE_MAS = 'page_mas'
    END_TITLE = 'end_title'
    TYP_ZONA = 'typ_zona'
    STREAM_RZ = 'stream_rz'
    BASE_FONT = 'base_font'
    FONT = 'font'
    CSS = 'css'
    CAPTION = 'caption'
    SIDEBAR_ICON = 'sidebar_icon'
    TABS = 'tabs'
    TAB = 'tab'


    # FACE = 'face'

class Config():
    def __init__(self, kod: int, user: UserDB, config: any):
        self._user = user
        self._config = config
        self.GRAPH_PAGE = [page[Names.PAGE_MAS] for page in self._config[Names.GRAPH_PAGE]]
        self.ALERTS = self._config[Names.MAS_ALERT]
        self.TITLES = self._config['mas_titles']
        self.GAG_TITLE = 'Заголовок не найден'
        
        # self._checkbox = bool(user)        
        kodes = [page['kod']  for page in self.GRAPH_PAGE] # все коды страниц
        self._kod = 0 if not user else kod # юзер не залогинен kod = 0        
        self._kod = 101 if self._kod != 0 and self._kod not in kodes else self._kod  # нет страницы вернем Главную kod = 101
        self._page_info = self.page_info()
        logger.debug(self._kod)

    def kod(self)-> int:
        return self._kod
    # def checkbox(self)-> bool:
    #     return self._checkbox
    def graph_page(self)->map:
        return self.GRAPH_PAGE
    def alerts(self)->map:
        return self.ALERTS    
    def alert(self, key: str)->map:
        return self.ALERTS[key]
    def menu(self)->list[map]:
        graph = self._config["graph"]
        graph = [menu["page_mas"] for menu in graph]
        menu_level1 = [menu for menu in graph if menu["kod_parent"] == 0]
        kod_level1 = [menu["kod"] for menu in menu_level1]
        menu_level2 = [menu for menu in graph if menu["kod_parent"] in kod_level1]
        return menu_level1 + menu_level2
    def has_dostup(self, item: map)-> bool:
        dostup = item.get('dostup',0)+1 # 1 - гость
        role_id = 0 if not self._user else self._user.role_id
        return role_id >= dostup
    def title_z1(self)-> str:
        return self._page_info[Names.TITLES][0]
    def title_z2(self)-> str:
        return self._page_info[Names.TITLES][1]
    def title_z3(self)-> str:
        return self._page_info[Names.TITLES][2]
    def background(self)->str:
        return self._page_info[Names.BACKGROUND]
    def design_background(self)->str:
        return self.image_path(self._config["face"])
    def icon(self)->list[str]:
        icons = self._page_info[Names.ICON]
        return None if len(icons) == 0 else [icons[0]]
    
    def page_info(self)->map:
        items = [item for item in self.graph_page() if item['kod']==self.kod]
        if len(items) == 0:
            return {Names.TITLES: [self.GAG_TITLE, self.GAG_TITLE, self.GAG_TITLE], Names.BACKGROUND: '', Names.ICON: [], Names.KOD: self._kod}            

        item = items[0]

        titles = item.get('titles', [])
        titles = [self.TITLES.get(t, self.GAG_TITLE) for t in titles]
        pic_rz = item.get('pic_rz',{})
        mas_pic_rz = self._config['mas_pic_rz'][str(pic_rz)]
        background = mas_pic_rz.get('background', None)
        icon = mas_pic_rz.get('icon', None)
        return {Names.TITLES: titles, Names.BACKGROUND: background, Names.ICON: icon, Names.KOD: self._kod}        
    def _alert(self, item: map):
        items = [page for page in self.graph_page() if page['kod']==item['ref']]
        # items = [item for item in self.GRAPH_PAGE if item['kod']==int(kod)]
        if len(items)!=1:
            return self.alert('1')
        if not self.has_dostup(item):
            return self.alert('2')
        return None

    def set_alert(self, item: map):
        typ_menu = item['typ_menu']
        if typ_menu == 'ref':
            alert = self._alert(item)
            if alert:
                # logger.debug(alert)                
                del item[typ_menu]
                item['typ_menu'] = 'alert'
                item['alert'] = alert
    def start_title(self):
        return self._config.get(Names.START_TITLE, self.GAG_TITLE)    
    def image_path(self, image):
        return image
        # return os.path.normpath("/".join([self.PATH_IMAGES, image]))

    def user(self):
        if not self._user:
            return None
        # user: # текущий пользователь (NULL при отсутствии ввода логина и пароля)
        # username: admin # а также - funct  и  operator
        # status: администратор # а также - соответственно - функционер и оператор
        # datetime: 01:56:13 # время работы зарегистрированного пользователя (от момента ввода параоля и до загрузки текущей формы)
        username = self._user[Names.USERNAME]
        status = ROLE_STATUS_MAP.get(self._user[Names.ROLE_ID], None)
        datetime_value = str(datetime.now())
        return {
            Names.USERNAME: username,
            Names.STATUS: status,
            Names.DATETIME: datetime_value,
        }
    def design(self):
        font = self._config[Names.BASE_FONT]
        css = self._config["kit_css"]  # ["main-0.css", "page-0.css"]  # список динамических стилей
        background = self.design_background()        
        
        footer = bool(self.user())
        caption = bool(self.user())
        checkbox = bool(self.user())
        sidebar = True

        return {
            Names.FONT: font, 
            Names.BACKGROUND: background, 
            Names.CAPTION: caption,
            Names.CHECKBOX: checkbox,
            Names.SIDEBAR: sidebar,
            Names.FOOTER: footer,
            Names.CSS: css}
    def sidebar_icon(self):
        return self._config[Names.VERH][Names.SIDEBAR_ICON]
    def verh_icons(self):
        verh = self._config[Names.VERH]
        if verh:
            return [self.image_path(icon) for icon in verh[Names.ICONS]]
        return []
    def background_rz0(self)-> str:
        return self.image_path(self._config['start_background_rz'])
    def brod(self):
        name = self.GAG_TITLE
        items = [item for item in self.GRAPH_PAGE if item['kod']==self._kod]
        if len(items) == 1:
            name = items[0]['name']

        menu = self.menu()

        items = [item for item in menu if item.get('ref',0)==self._kod]
        if len(items)==0:
            return name
        kod = items[0]['kod']
        kod_menu = {item['kod']:item for item in menu }
        res = [name]
        while True:
            item = kod_menu.get(kod,None)
            if not item:
                break
            kod = item['kod_parent']
            res.append(item['name'])
        return " / ".join(res[::-1])
    def workzona_tabs(self):
        return self._config['gen_work_zona'][Names.TABS]
    def workzona(self):
        return self._config['gen_work_zona']


class Element:
    def __init__(self, config: Config):
        self.config = config
    @abstractmethod
    def get():
        pass
    def __call__(self):
        return self.get()

class PageSidebar(Element):
#     verh: # Область ввода и визуализации логина и пароля
#     navi : # Область наигации по открытм страницам Системы
#     kratko : ЗНАЧЕНИЕ # Краткая информация об ОТКРЫТОЙ странице
#     active_tab: ЗНАЧЕНИЕ
#     tabs : [] # Область ввода и визуализации логина и пароля
#       - tab: 
#         name: Справка # таких элементов - три: Справка, Фильтры, Опции *******
#         typ_tab: vis | hide | hide_none # vis - та, которая видима (active_tab), hide - которые НЕвидлимы, но активны  hide_none - которые НЕвидимы и НЕактивны
# # смена панелеей, в отличие от рабочей зоны, делается БЕЗ ПЕРЕЗАГРУЗКИ - только visible и hide, с изменением покраски заголовкоы
# # а все массивы нижеследующие - даже ПУСТЫЕ и- прорисовываются СРАЗУЖЕ, при загрузке страницы
#         help: [] # массив пЕРЕМЕННОЙ длины
#         filtr: [] # массив пЕРЕМЕННОЙ длины или NULL
#         key: []  массив пЕРЕМЕННОЙ длины или NULL

    def get(self):
        return {Names.USER: self.config.user()}
        # return {Names.USER: self.config.user(), Names.CHECKBOX: self.config.checkbox()}

class PageWorkZona(Element):
    # title: заголовок
    # background: pic # фон
    # icon: pic|null # иконка справа в шапке
    # tabs: null | # или массив пЕРЕМЕННОЙ длины
    # end_title: ЗНАЧЕНИЕ или NULL
    # data : # данные страницы
    # typ_rz: rows|list|table|org|vvod|data ... # Схема ТА ЖЕ, что и для элемента меню - в переменной лежит ИМЯ МАССИВА     

    def _rz(self):
        pass
        # kod = page_info['kod']
        # # data : # Данные страницы ****
        # # typ_rz: rows|list|table|org|vvod|data ... # Схема ТА ЖЕ, что и для элемента меню - в переменной лежит ИМЯ МАССИВА     
        # # rows:
        # stream_rz = self.config[Names.STREAM_RZ]
        # stream_rz = [rz['mas_type'] for rz in stream_rz]

    def get(self):
        title = self.config.title_z2()
        end_title = self.config.title_z3()
        background = self.config.background()
        icon =  self.config.icon()
        tabs = self.config.workzona_tabs()
        logger.debug(tabs)
        # typ_zona = self.page_info['typ_zona']
        return {
            Names.BACKGROUND: background,
            Names.ICON: icon,
            Names.TITLE: title,
            Names.END_TITLE: end_title,
            Names.TABS: tabs
            # Names.TYP_ZONA: typ_zona
        }

class PageMenu(Element):
    def get(self):
        menu = self.config.menu()
        for item in menu:
            self.config.set_alert(item)
        return menu

class BasePage(Element):
    def _verh(self):
        title = self.config.start_title()
        icons = self.config.verh_icons()
        sidebar_icon = self.config.sidebar_icon()
        return {Names.TITLE: title, Names.ICONS: icons, Names.SIDEBAR_ICON: sidebar_icon}
    def _menu(self):
        return PageMenu(self.config)()
    def _head(self):
        active_menu = 1
        ins = {Names.ORGSTR: "структура", Names.BROD: self.config.brod()}
        return {
            Names.ACTIVE_MENU: active_menu,
            Names.INS: ins,
            Names.MENU: self._menu(),
        }

    def _sidebar(self):
        return PageSidebar(self.config)() 

    def _work_zona(self):
        return self.config.workzona()
        # return PageWorkZona(self.config)()

    def _footer(self):
        return None

    def get(self):
        return {
            Names.DESIGN: self.config.design(), # свойства дизайна
            Names.VERH: self._verh(),  # заголовок
            Names.HEAD: self._head(),  # шапка
            Names.SIDEBAR: self._sidebar(),  # боковик
            Names.WORK_ZONA: self._work_zona(),  # рабочая
            Names.FOOTER: self._footer()  # подвал
        }

class Page0(BasePage):
    # page: 0
    # При ПЕРВИЧНОМ старте и при клику по кнопке «Выход» стартует ПЕРЕРИСОВКА страницы, при этом
    # •	загружается ПУСТАЯ рабочая область- или она СТИРАЕТСЯ (если это выход. ХОТЯ: решайте сами – может быть и всегда просто ПЕРЕгруз);
    # •	Полоска экрана, где стоит чекбоксы и крестик – прячется
    # •	Сам чек бокс Главного Меню – становится пустым;
    # •	Заголовок страницы и заливка рабочей зоны – берутся из общих данных (из yaml – см. п. .
    # •	После ввода пароля – восстанавливается «нормальный вид (главное и подвал – видны)

    # Все прочие (кроме 0) страницы - по оговоренному сценарию (чем мы сейчас и занимаемся). Нулевая же - это совсем иная песня, Это:
    # *** заголовок, подвал, боковая панель без чек-боксов и крестика закрытия боковой панели;
    # *** главное меню спрятано (или  нет совсем на нулевой странице - так даже лучше);
    # *** и чек-боксы - тоже можно с нулевой снести к лешему вообще;
    # *** в рабочей области - только фон залит, больше - вообще ничего нет;
    # *** назначение нулевой - ввод пароля НА ПУСТОМ, фактически месте (как описано выше), ВНЕ какой-либо возможности что-либо сломать или испортить
    # *** результат авторизации - загрузка страницы 101.
    def _user(self):
        return None
    def _sidebar(self):
        return PageSidebar(self.config)() 
    def _menu(self):
        return []
    def _head(self):
        ins = {Names.ORGSTR: "структура", Names.BROD: ''}
        return {
            # Names.ACTIVE_MENU: 1,
            Names.INS: ins,
            Names.MENU: [],
        }
    def _work_zona(self):
        return {Names.BACKGROUND: self.config.background_rz0()}

class Page(BasePage):
    pass


@router.get("/{kod}", response_model=page.Page)
async def page(request: Request, kod: int = Path(..., gt=-1)) -> page.Page:
    user: UserDB = await security.get_current_user(request)
    config = Config(kod, user, config_doc)
    page = Page0(config) if not user else Page(config)
    # page = PageModel.parse_obj(page())
    # return page.json()
    return page()
