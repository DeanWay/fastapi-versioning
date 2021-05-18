from typing import List

from fastapi.routing import APIRouter
from pydantic import BaseModel

from fastapi_versioning import version

router = APIRouter()


class Item(BaseModel):
    id: str
    name: str
    price: float


class ItemV1(Item):
    quantity: int


class ComplexQuantity(BaseModel):
    store_id: str
    quantity: int


class ItemV2(Item):
    quantity: List[ComplexQuantity]


@router.get("/item/{item_id}", response_model=ItemV1)
@version(1, 1)
def get_item_v1(item_id: str) -> ItemV1:
    return ItemV1(
        id=item_id,
        name="ice cream",
        price=1.2,
        quantity=5,
    )


@router.get("/item/{item_id}", response_model=ItemV2)
@version(1, 2)
def get_item_v2(item_id: str) -> ItemV2:
    return ItemV2(
        id=item_id,
        name="ice cream",
        price=1.2,
        quantity=[{"store_id": "1", "quantity": 5}],
    )


@router.delete("/item/{item_id}")
@version(1, 2)
def delete_item(item_id: str) -> None:
    return None


@router.post("/item", response_model=ItemV2)
@version(1, 3)
def create_item(item: ItemV2) -> ItemV2:
    return item
