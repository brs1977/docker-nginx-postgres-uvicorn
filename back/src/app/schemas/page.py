from __future__ import annotations
from typing import Any, Optional, Union

from pydantic import BaseModel, Field, Extra


class AppModel(BaseModel):

  def dict(self, *args, **kwargs):
    if kwargs and kwargs.get("exclude_none") is not None:
      kwargs["exclude_none"] = True
      return BaseModel.dict(self, *args, **kwargs)


class Design(BaseModel):
    font: int
    background: str
    footer: bool
    caption: bool
    checkbox: bool 
    sidebar: bool
    css: list[str]


class Verh(BaseModel):
    title: str
    sidebar_icon: str
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
    typ_menu: str
    ref: Optional[int] = None
    sub: Optional[int] = None
    alert: Optional[Alert] = None


class Head(AppModel):
    active_menu: Optional[int]
    ins: Ins
    menu: list[MenuItem] = []

class User(BaseModel):
    username: str
    status: str
    datetime: str


class Sidebar(BaseModel):
    user: Optional[User] = Field(..., nullable=True)
    # checkbox: bool

class Tab(BaseModel):
    name: str
    active: int
    ref: list[int] = []

class WorkZona(BaseModel):
    background: Optional[str] = Field(default=None, nullable=True)
    icon: Optional[list[str]] = Field(default=None, nullable=True)
    title: Optional[str] = Field(default=None, nullable=True)
    end_title: Optional[str] = Field(default=None, nullable=True)
    tabs: list[Tab] = Field(default=None, nullable=True)
    # class Config:
    #     extra = Extra.allow


class Page(BaseModel):
    design: Design
    verh: Verh
    head: Head
    sidebar: Sidebar
    work_zona: WorkZona
    footer: Any = Field(..., nullable=True)
