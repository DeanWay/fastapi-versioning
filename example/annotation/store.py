from typing import NoReturn

from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel
from typing_extensions import Literal

from fastapi_versioning import version

router = APIRouter()


class StoreCommon(BaseModel):
    id: str
    name: str
    country: str


class StoreV1(StoreCommon):
    status: bool


class StoreV2(StoreCommon):
    status: Literal["open", "closed", "closed_permanently"]


@router.get("/store/{store_id}", response_model=StoreV1)
def get_store_v1(store_id: str) -> StoreV1:
    return StoreV1(
        id=store_id,
        name="ice cream shoppe",
        country="Canada",
        status=True,
    )


@router.get("/store/{store_id}", response_model=StoreV2)
@version(1, 1)
def get_store_v2(store_id: str) -> StoreV2:
    return StoreV2(
        id=store_id,
        name="ice cream shoppe",
        country="Canada",
        status="open",
    )


@router.get("/store/{store_id}", include_in_schema=False)
@version(1, 3)
def get_store_v3(store_id: str) -> NoReturn:
    raise HTTPException(status_code=404)
