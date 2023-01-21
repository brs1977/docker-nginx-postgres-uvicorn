from fastapi import APIRouter, HTTPException, Path, Response
from app.api.v1.config.utils import read_config, get_menu, get_bp_niz, get_menu_page
from loguru import logger

router = APIRouter()

config = read_config()

def get_ins(config_doc):
    return config_doc['ins']

@router.get("/ins", status_code=201)
async def menu():
    try:
        return get_ins(config)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/menu", status_code=201)
async def menu():
    try:
        return get_menu(config)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/bp_niz", status_code=201)
async def bp_niz():
    try:
        return get_bp_niz(config)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/menu/{kod}/", status_code=201)
async def page(kod: int = Path(..., gt=0)):

    if kod == 1:
        media_type = "application/json"
        content = str(get_menu_page(config, kod))
        return Response(content=content, media_type=media_type)
    else:
        media_type = "plain/text"
        content = get_menu_page(config, kod)
        return Response(content=content, media_type=media_type)
