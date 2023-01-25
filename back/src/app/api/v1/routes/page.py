from fastapi import Path, APIRouter, status, HTTPException, Depends
from app.api.v1.config.utils import read_config
from app.schemas.users import UserDB
from abc import abstractmethod
import pandas as pd
from loguru import logger
from enum import Enum

config = read_config()
router = APIRouter()


class Names(Enum):
    DESIGN = "design"
    USER = "user"
    VERH = "verh"
    HEAD = "head"
    SIDEBAR = "sidebar"
    WORK_ZONA = "work_zona"
    FOOTER = "footer"
    TITLE = "title"
    BACKGROUND = "background"
    ICONS = 'icons'
    ICON = 'icon'
    ORGSTR = "orgstr"
    BROD = "brod"
    INS = "ins"
    ACTIVE_MENU = "active_menu"
    MENU = "menu"
    MENU_TYPE = 'menu_typ'
    ALERT = 'alert'
    REF = 'ref'
    SUB = 'sub'
    PAGE = 'page'
    KOD = 'kod'


class Alert:
    COMPONENT_NOT_FOUND = {
        "title": "НЕ найден компонент",
        "text": "Вызываемая страница не найдена или находится в состоянии доработки и временно отключена от Системы. Обращайтесь к администратору Системы",
    }

class Element:
    def __init__(self, config: any):
        self.config = config
    @abstractmethod
    def get():
        pass
    def __call__(self):
        return self.get()

class WorkZona(Element):
    
    def type_main():
    # if kod == 101:
    #     for page in config_doc["stream-rz"]["typ-1"]:
    #         if page["page"]["kod"] == kod:
    #             item = page["page"]
    #             item["type"] = 1
    #             return item
        return {}

    def get(self):
        #   title: заголовок
        #   background: pic # фон
        #   icon: pic|null # иконка справа в шапке
        #   end_title: ЗНАЧЕНИЕ или NULL
        #   typ_content: tabs|list
        pass

class Menu(Element):
    def get(self):
        graph = self.config["graph"]
        graph = [ menu['page'] for menu in graph]
        menu_1_level = [menu for menu in graph if menu['kod_parent']==0]
        kod_1_level = [menu['kod'] for menu in menu_1_level ]
        menu_2_level = [menu for menu in graph if menu['kod_parent'] in kod_1_level]
        menu = menu_1_level + menu_2_level        
        return menu


# class Menu(Element):
#     def __init__(self, config: any):
#         super().__init__(config)
#         self._menus = None
#         self._df_graph = None

#     @property
#     def graph(self) -> pd.DataFrame:
#         # kod	kod_parent	name	typ_page	dostup	long-zag	typ-rz	tabs-rz
#         if not self._df_graph is None:
#             return self._df_graph

#         df = [item["page"] for item in self.config["graph"]]
#         self._df_graph = pd.DataFrame(df)
#         self._df_graph["has_child"] = self._df_graph.kod.apply(
#             lambda x: int(self._df_graph.kod_parent.isin([x]).any())
#         )
#         return self._df_graph

#     def _raw_menu(self):
#         return (
#             self.graph[self.graph["typ_page"].isin([1, 2])]
#             .loc[:, ["kod", "kod_parent", "name", "has_child", "typ_page"]]
#             .to_dict("records")
#         )

#     def _alert(self, type: int, item: any):
#         if type == 1:
#             item[Names.MENU_TYPE] = Names.ALERT
#             item[Names.ALERT] = Alert.COMPONENT_NOT_FOUND
#             return item

#     def _ref(self, kod: int, item: any):
#         item[Names.MENU_TYPE] = Names.REF
#         item[Names.REF] = {Names.PAGE: kod}
#         # return item

#     def _sub(self, item: any):
#         item[Names.MENU_TYPE] = Names.SUB
#         item[Names.SUB] = {Names.KOD: item["kod"]}
#         return item

#     def _item(self, item):
#         # # элемент меню
#         # menu:
#         #   kod: 1
#         #   kod_parent: 0
#         #   name: "Главная"
#         #   typ_menu:  ref|sub|alert (ссылка|подменю|сообщение)

#         rows = self.graph[self.graph["kod_parent"] == item["kod"]]
#         if rows.empty:
#             self._alert(1, item)
#         else:
#             # print(item['kod'], rows.iloc[0]['typ_page'], rows.typ_page.iloc[0])
#             if rows.typ_page.iloc[0] == 4:
#                 if len(rows) == 1:
#                     self._ref(int(rows.kod.iloc[0]), item)
#                 else:
#                     self._alert(1, item)
#             else:
#                 self._sub(item)

#         del item["has_child"]
#         del item["typ_page"]
#         return item

#     def get(self):
#         return [self._item(menu) for menu in self._raw_menu()]


class Page(Element):
    def __init__(self, kod: int, config: any, user: UserDB):
        super().__init__(config)
        self.kod = kod
        self.config = config
        self.user = user
        self.data = {}

    def _design(self):
        font = 15
        css =  self.config['kit-css'] # ["main-0.css", "page-0.css"]  # список динамических стилей
        self.data[Names.DESIGN] = {"font": font, "css": css}

    def _user(self):
        self.data[Names.USER] = self.user

    def _verh(self):
        def icons():
            verh = self.config["verh"]
            if verh:
                return verh['icons']
            return []
        gag_title = 'Заголовок не найден'
        titles = self.config["mas_titles"]
        title = titles.get(str(self.kod), gag_title)
        
        icons = icons()
        self.data[Names.VERH] = {Names.TITLE: title, Names.ICONS: icons}

    def _head(self):
        active_menu = 1
        ins = {Names.ORGSTR: "структура", Names.BROD: "крошки"}

        menu = Menu(self.config)
        self.data[Names.HEAD] = {
            Names.ACTIVE_MENU: active_menu,
            Names.INS: ins,
            Names.MENU: menu(),
        }

    def _sidebar(self):
        self.data[Names.SIDEBAR] = {}

    def _work_zona(self):
        self.data[Names.WORK_ZONA] = {}

    def _footer(self):
        self.data[Names.FOOTER] = {}

    def get(self):
        self._design()
        self._user()
        self._verh()  # заголовок
        self._head()  # шапка
        self._sidebar()  # боковик
        self._work_zona()  # рабочая
        self._footer()  # подвал

        return self.data


# page:
#   design:
#     font: 15
#     css: [nain-0.css,page-0.css, ..] # список динамических стилей
#   user: null | 	{username,status,datetime} #текущий пользователь
#   verh: #заголовок
#   head: #шапка
#   sidebar: #боковик
#   work_zona: #рабочая
#   footer: #подвал


@router.get("/{kod}")
async def page(kod: int = Path(..., gt=0), user: UserDB = None): #Depends(security.get_page_user)):
    page = Page(kod, config, user)
    return page()
