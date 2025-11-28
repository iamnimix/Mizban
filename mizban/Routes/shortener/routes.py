import pathlib
import sys

from fastapi import APIRouter, Depends, Request, HTTPException, Path
from fastapi.responses import RedirectResponse
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(ROOT_DIR))

from mizban.Core.utils import generate_short_code
from mizban.Core.dependencies import get_db
from mizban.Core.models import URL
from .schema import RequestUrl, ResponseUrl



router = APIRouter()



@router.post('/shorten')
async def create_short_url(data: RequestUrl, request: Request, db: AsyncSession = Depends(get_db)):
    check_url = await db.execute(select(URL).where(URL.original_url == str(data.url)))
    existing = check_url.scalar_one_or_none()
    if existing:
        short_url = f"{request.base_url}{existing.short_code}"
        return {"short_url": f"{short_url}"}

    while True:
        code = generate_short_code()
        res = await db.execute(select(URL).where(URL.short_code == code))
        if not res.scalar_one_or_none():
            break

    short_url = f"{request.base_url}{code}"

    new_url = URL(original_url=str(data.url), short_code=code)
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)

    return {"short_url": short_url}





@router.get('/{short_code}')
async def redirect_to_original(short_code: Annotated[str, Path(max_length=5)], db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(URL).where(URL.short_code == short_code))
    url = result.scalar_one_or_none()

    if not url:
        raise HTTPException(status_code=404, detail="URL Not Found")

    return RedirectResponse(url=url.original_url)


