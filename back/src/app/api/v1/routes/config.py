from fastapi import APIRouter, HTTPException
from app.api.v1.config.utils import read_config, get_menu, get_bp_niz
from loguru import logger

router = APIRouter()

config = read_config()


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
