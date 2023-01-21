from fastapi import Path, APIRouter, status, HTTPException, Depends
from app.api.v1.config.utils import read_config
import pandas as pd
from loguru import logger

config = read_config()

router = APIRouter()

def extract_map(config_doc, name):
    return {int(k): str.strip(v) for k, v in [el.split(";") for el in config_doc[name]]}

  
def get_all_menu(config_doc):
    # kod	kod_parent	name	typ_page	dostup	long-zag	typ-rz	tabs-rz
    df_graph = [item["page"] for item in config_doc["graph"]]
    df_graph = pd.DataFrame(df_graph)
    # types = {col:'int32' for col in df_graph.select_dtypes('int').columns}
    # df_graph = df_graph.astype(types)    

    # df_graph["parent"] = df_graph.kod // 100
    # df_graph = df_graph.loc[:, ["kod", "parent", "name", "typ", "dost"]]
    df_graph["has_child"] = df_graph.kod.apply(lambda x: int(df_graph.kod_parent.isin([x]).any()))

    menus = (
        df_graph[df_graph["typ_page"].isin([1, 2])]
        .loc[:, ["kod", "kod_parent", "name", "has_child", "typ_page"]]
        .to_dict("records")
    )

    for menu in menus:
        rows = df_graph[df_graph['kod_parent']==menu['kod']]
        if rows.empty:
            menu["action"] = {
                "type": "alert",
                "title": "Ошибка структуры",
                "text": f"Не задана рабочая область kod:{menu['kod']}",
            }
        else:
            if rows.iloc[0]['typ_page'] == 2:
                continue
            elif rows.typ_page.iloc[0]==4:
                if len(rows) == 1:
                    menu['action'] = {'type':'page', 'page':int(rows.kod.iloc[0])}
                else:
                    menu["action"] = {
                        "type": "alert",
                        "title": "Ошибка структуры",
                        "text": f"Уровень kod:{menu['kod']} содержит несколько потомков",
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
    # return {}

@router.get("/{kod}/ins")
def ins(kod: int = Path(..., gt=0)):
    return config["ins"]


@router.get("/{kod}")
async def menu(kod: int = Path(..., gt=0)):
    return get_menu(kod, config)
