from fastapi import Path, APIRouter, status, HTTPException, Depends
from app.api.v1.config.utils import read_config

config = read_config()

router = APIRouter()

def get_menu(kod, config_doc):
    for page in config_doc['stream-rz']['typ-1']:
        if page['page']['kod'] == kod:
            item = page['page']
            item['type'] =  1
            return item
    

@router.get("/{kod}")
async def menu(kod: int = Path(..., gt=0)):
    return get_menu(101, config)
