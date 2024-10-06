from fastapi import APIRouter
from loguru import logger

router = APIRouter(tags=["cart"], prefix="/cart")


@router.get("/")
def get_cart_content():
    pass


@router.post("/")
def add_item():
    pass


@router.delete("/")
def remove_item():
    pass


@router.patch("/")
def toggle_select():
    pass
