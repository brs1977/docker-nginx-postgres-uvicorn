from fastapi import Request, Path, APIRouter, status, HTTPException, Depends
from app.api.v1.config.utils import read_config
from app.schemas.users import UserDB
from app.schemas.page import *
from app.api import security
from datetime import datetime
from abc import abstractmethod
from loguru import logger
from enum import Enum, EnumMeta
import os

config = read_config()
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


    # FACE = 'face'

class Element:
    def __init__(self, config: any):
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

    def __init__(self, config: any, user: map, checkbox: bool = True):
        self.user = user
        self.checkbox = checkbox
        super().__init__(config)        
    def get(self):
        return {Names.USER: self.user, Names.CHECKBOX: self.checkbox}

class PageWorkZona(Element):
    # title: заголовок
    # background: pic # фон
    # icon: pic|null # иконка справа в шапке
    # tabs: null | # или массив пЕРЕМЕННОЙ длины
    # end_title: ЗНАЧЕНИЕ или NULL
    # data : # данные страницы
    # typ_rz: rows|list|table|org|vvod|data ... # Схема ТА ЖЕ, что и для элемента меню - в переменной лежит ИМЯ МАССИВА     

    def __init__(self, config: any, page_info: map):
        self.page_info = page_info
        super().__init__(config)        

    def _icon(self, icons: list[str]):
        return None if len(icons) == 0 else [icons[0]]
    def _rz(self):
        kod = page_info['kod']
        # data : # Данные страницы ****
        # typ_rz: rows|list|table|org|vvod|data ... # Схема ТА ЖЕ, что и для элемента меню - в переменной лежит ИМЯ МАССИВА     
        # rows:
        stream_rz = self.config[Names.STREAM_RZ]
        stream_rz = [rz['mas_type'] for rz in stream_rz]
  - mas_typ:
      typ: rows
      data_typ:
]
  - mas_typ:
      typ: rows
      data_typ:

    def get(self):
        title = self.page_info[Names.TITLES][1]
        end_title = self.page_info[Names.TITLES][2]
        background = self.page_info[Names.BACKGROUND]
        icon = self._icon(self.page_info[Names.ICON])
        # typ_zona = self.page_info['typ_zona']
        return {
            Names.BACKGROUND: background,
            Names.ICON: icon,
            Names.TITLE: title,
            Names.END_TITLE: end_title,
            # Names.TYP_ZONA: typ_zona
        }

class Alert1Exception(Exception):
    pass
class Alert2Exception(Exception):
    pass    


class PageMenu(Element):
    def __init__(self, config: any, user: UserDB):
        super().__init__(config)
        self.user = user
        self.GRAPH_PAGE = [page[Names.PAGE_MAS] for page in self.config[Names.GRAPH_PAGE]]
        self.ALERTS = config[Names.MAS_ALERT]

    def _alert(self, item: map):
        items = [page for page in self.GRAPH_PAGE if page['kod']==item['ref']]
        # items = [item for item in self.GRAPH_PAGE if item['kod']==int(kod)]
        if len(items)!=1:
            return self.ALERTS['1']
        dostup = item.get('dostup',0)+1 # 1 - гость
        role_id = 0 if not self.user else self.user.role_id
        if dostup > role_id:
            return self.ALERTS['2']
        return None

    def get(self):
        graph = self.config["graph"]
        graph = [menu["page_mas"] for menu in graph]
        menu_level1 = [menu for menu in graph if menu["kod_parent"] == 0]
        kod_level1 = [menu["kod"] for menu in menu_level1]
        menu_level2 = [menu for menu in graph if menu["kod_parent"] in kod_level1]
        menu = menu_level1 + menu_level2
        for item in menu:
            typ_menu = item['typ_menu']
            if typ_menu == 'ref':
                alert = self._alert(item)
                if alert:
                    # logger.debug(alert)                
                    del item[typ_menu]
                    item['typ_menu'] = 'alert'
                    item['alert'] = alert
        return menu

class BasePage(Element):
    def __init__(self, kod: int, config: any, user: UserDB):
        super().__init__(config)
        self.kod = kod
        self.config = config
        self.user = user
        self.PATH_IMAGES = self.config[Names.PATH_IMAGES]        

        self.TITLES = self.config[Names.MAS_TITLES]
        self.ALERTS = self.config[Names.MAS_ALERT]
        self.GRAPH_PAGE = [page[Names.PAGE_MAS] for page in self.config[Names.GRAPH_PAGE]]
        self.GAG_TITLE = "Заголовок не найден"
        
        kodes = [page['kod']  for page in self.GRAPH_PAGE]
        if self.kod not in kodes:
            self.kod = 101



        # self.page_info = self._page_info()

    def _page_info(self):
        items = [item for item in self.GRAPH_PAGE if item['kod']==self.kod]
        if len(items)!=1:
            raise Alert1Exception() 
        item = items[0]

        titles = item.get('titles', [])
        TITLES = self.config['mas_titles']
        titles = [TITLES.get(t, self.GAG_TITLE) for t in titles]
 
        dostup = item['dostup']+1 # 1 - гость
        role_id = 0 if not self.user else self.user.role_id
        if dostup > role_id:
            raise Alert2Exception() 

        pic_rz = item.get('pic_rz',{})
        mas_pic_rz = self.config['mas_pic_rz'][str(pic_rz)]
        background = mas_pic_rz.get('background', None)
        icon = mas_pic_rz.get('icon', None)
        return {Names.TITLES: titles, Names.BACKGROUND: background, Names.ICON: icon, 'kod': self.kod}


    def _image_path(self, image):
        return image
        # return os.path.normpath("/".join([self.PATH_IMAGES, image]))
    def _title_z1(self):
        return self.config.get(Names.START_TITLE, self.GAG_TITLE)    
    def _title_z2(self):
        return self.TITLES.get(str(self.kod), self.GAG_TITLE)
    def _design(self):
        font = 15
        css = self.config["kit_css"]  # ["main-0.css", "page-0.css"]  # список динамических стилей
        background = self._image_path(self.config["face"])
        return {"font": font, Names.BACKGROUND: background, "css": css}
    def _verh(self):
        def icons():
            verh = self.config[Names.VERH]
            if verh:
                return [self._image_path(icon) for icon in verh[Names.ICONS]]
            return []

        title = self._title_z1()
        icons = icons()
        return {Names.TITLE: title, Names.ICONS: icons}

    def _user(self):
        # user: # текущий пользователь (NULL при отсутствии ввода логина и пароля)
        # username: admin # а также - funct  и  operator
        # status: администратор # а также - соответственно - функционер и оператор
        # datetime: 01:56:13 # время работы зарегистрированного пользователя (от момента ввода параоля и до загрузки текущей формы)
        username = self.user[Names.USERNAME]
        status = ROLE_STATUS_MAP.get(self.user[Names.ROLE_ID], None)
        datetime_value = str(datetime.now())
        return {
            Names.USERNAME: username,
            Names.STATUS: status,
            Names.DATETIME: datetime_value,
        }

    def _menu(self):
        return PageMenu(self.config, self.user)()

    def _head(self):
        active_menu = 1
        ins = {Names.ORGSTR: "структура", Names.BROD: "крошки"}
        return {
            Names.ACTIVE_MENU: active_menu,
            Names.INS: ins,
            Names.MENU: self._menu(),
        }

    def _sidebar(self):
        return PageSidebar(self.config, self._user())() 

    def _work_zona(self):
        return PageWorkZona(self.config, self._page_info())()

    def _footer(self):
        return None

    def get(self):
        return {
            Names.DESIGN: self._design(), # свойства дизайна
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
        return PageSidebar(self.config, self._user(), False)() 
    def _menu(self):
        return None
    def _work_zona(self):
        return {Names.BACKGROUND: self._image_path(self.config['start_background_rz'])}

class Page(BasePage):
    pass


@router.get("/{kod}", response_model=PageModel)
async def page(request: Request, kod: int = Path(..., gt=0)) -> PageModel:
    user: UserDB = await security.get_current_user(request)
    page = Page0(kod, config, user) if not user else Page(kod, config, user)
    # page = PageModel.parse_obj(page())
    # return page.json()
    return page()
