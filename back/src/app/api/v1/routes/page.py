from fastapi import Path, APIRouter, status, HTTPException, Depends
from app.api.v1.config.utils import read_config
from app.schemas.users import UserDB
from app.api import security
from datetime import datetime
from abc import abstractmethod
import pandas as pd
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


#     @classmethod
#     def is_names(cls, names):
#         if isinstance(color, cls):
#             names=names.value
#         if not names in cls.__members__:
#             return False
#         else:
#             return True

# class NamesDict(dict):
#     def __setitem__(self, k, v):
#         if isinstance(k, Enum):
#             k = k.value
#         super().__setitem__(k.value, v)

#     def __getitem__(self, k):
#         if isinstance(k, Enum):
#             k = k.value
#         return super().__getitem__(k)


# class Alert:
#     COMPONENT_NOT_FOUND = {
#         "title": "НЕ найден компонент",
#         "text": "Вызываемая страница не найдена или находится в состоянии доработки и временно отключена от Системы. Обращайтесь к администратору Системы",
#     }


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
        graph = [menu["page"] for menu in graph]
        menu_level1 = [menu for menu in graph if menu["kod_parent"] == 0]
        kod_level1 = [menu["kod"] for menu in menu_level1]
        menu_level2 = [menu for menu in graph if menu["kod_parent"] in kod_level1]
        menu = menu_level1 + menu_level2
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
        self.PATH_IMAGES = self.config[Names.PATH_IMAGES]
        self.data = {}

        self.TITLES = self.config[Names.MAS_TITLES]
        self.ALERTS = self.config[Names.MAS_ALERT]
        self.GAG_TITLE = "Заголовок не найден"

    def _image_path(self, image):
        return os.path.normpath("/".join([self.PATH_IMAGES, image]))

    def _design(self):
        font = 15
        css = self.config["kit-css"]  # ["main-0.css", "page-0.css"]  # список динамических стилей
        face = self._image_path(self.config["face"])
        self.data[Names.DESIGN] = {"font": font, "face": face, "css": css}

    def _user(self):
        # user: # текущий пользователь (NULL при отсутствии ввода логина и пароля)
        # username: admin # а также - funct  и  operator
        # status: администратор # а также - соответственно - функционер и оператор
        # datetime: 01:56:13 # время работы зарегистрированного пользователя (от момента ввода параоля и до загрузки текущей формы)
        username = self.user[Names.USERNAME]
        status = ROLE_STATUS_MAP.get(self.user[Names.ROLE_ID], None)
        datetime_value = datetime.now()
        self.data[Names.USER] = {
            Names.USERNAME: username,
            Names.STATUS: status,
            Names.DATETIME: datetime_value,
        }

    def _title_z1(self):
        return self.TITLES.get(str(self.kod), self.GAG_TITLE)

    def _verh(self):
        def icons():
            verh = self.config[Names.VERH]
            if verh:
                return [self._image_path(icon) for icon in verh[Names.ICONS]]
            return []

        title = self._title_z1()
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
async def page(kod: int = Path(..., gt=0), user: UserDB = Depends(security.manager)):
    page = Page(kod, config, user)
    return page()
