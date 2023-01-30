from __future__ import annotations
from typing import Any, Optional

from pydantic import BaseModel


class AppModel(BaseModel):

  def dict(self, *args, **kwargs):
    if kwargs and kwargs.get("exclude_none") is not None:
      kwargs["exclude_none"] = True
      return BaseModel.dict(self, *args, **kwargs)


class Design(BaseModel):
    font: int
    background: str
    css: list[str]


class Verh(BaseModel):
    title: str
    icons: list[str]


class Ins(BaseModel):
    orgstr: str
    brod: str



class Alert(BaseModel):
    title: str
    text: str

class MenuItem(AppModel):
    kod: int
    kod_parent: int
    name: str
    typ_menu: Optional[str] = None
    ref: Optional[int] = None
    sub: Optional[int] = None
    alert: Optional[Alert] = None


class Head(BaseModel):
    active_menu: int
    ins: Ins
    menu: list[MenuItem] = None


class User(BaseModel):
    username: str
    status: str
    datetime: str


class Sidebar(BaseModel):
    user: Optional[User] = None
    checkbox: bool


class WorkZona(BaseModel):
    background: str = None
    icon: list[str] = None
    title: str = None
    end_title: Any


class PageModel(BaseModel):
    design: Design
    verh: Verh
    head: Head
    sidebar: Sidebar
    work_zona: WorkZona
    footer: Any
