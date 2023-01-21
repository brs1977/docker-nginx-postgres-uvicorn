from fastapi import Path, APIRouter, status, HTTPException, Depends
from app.api.v1.config.utils import read_config
import pandas as pd

config = read_config()

router = APIRouter()


def extract_map(config_doc, name):
    return {int(k): str.strip(v) for k, v in [el.split(";") for el in config_doc[name]]}


def get_all_menu(config_doc):
    # kod	kod-parent	name	typ-page	dostup	long-zag	typ-rz	tabs-rz
    df_graph = [item["page"] for item in config_doc["graph"]]
    df_graph = pd.DataFrame(df_graph)

    df_graph["parent"] = df_graph.kod // 100

    # df_graph = df_graph.loc[:, ["kod", "parent", "name", "typ", "dost"]]
    df_graph["has_child"] = df_graph.kod.apply(lambda x: int(df_graph.parent.isin([x]).any()))

    menus = (
        df_graph[df_graph["typ-page"].isin([1, 2])]
        .loc[:, ["kod", "parent", "name", "has_child"]]
        .to_dict("records")
    )

    for menu in menus:
        if menu["has_child"] == 0:
            menu["action"] = {
                "type": "alert",
                "title": "Ошибка структуры",
                "text": f"Не задана рабочая область kod:{menu['kod']}",
            }
        if menu["kod"] == 1:
            menu["action"] = {"type": "page"}
        if menu["kod"] == 10:
            menu["action"] = {
                "type": "alert",
                "title": "Ошибка структуры",
                "text": f"Не задана рабочая область kod:{menu['kod']}",
            }

    return menus


def get_menu(kod, config_doc):
    if kod == 101:
        for page in config_doc["stream-rz"]["typ-1"]:
            if page["page"]["kod"] == kod:
                item = page["page"]
                item["type"] = 1
                return item
    elif kod == 20101:
        for page in config_doc["stream-rz"]["typ-2"]:
            if page["page"]["kod"] == kod:
                item = page["page"]
                item["type"] = 2
                return item
    else:
        raise HTTPException(status_code=404, detail=f"Page {kod} not found")


@router.get("")
async def all_menu():
    return get_all_menu(config)


@router.get("/{kod}")
async def menu(kod: int = Path(..., gt=0)):
    return get_menu(kod, config)
