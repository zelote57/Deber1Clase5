from fastapi import APIRouter, HTTPException, Response, status

from db.database import SessionDep
from dependencies.auth import CurrentUser
from schemas.product import ProductCreate, ProductRead, ProductUpdate
from services import product_service

router = APIRouter(tags=["Products"], prefix="/products")


def raise_product_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado.",
    )


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    data: ProductCreate,
    current_user: CurrentUser,
    session: SessionDep,
):
    return product_service.create_product(data, current_user.id, session)


@router.get("/", response_model=list[ProductRead])
def get_products(current_user: CurrentUser, session: SessionDep):
    return product_service.get_products(current_user.id, session)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    current_user: CurrentUser,
    session: SessionDep,
):
    product = product_service.get_product(
        product_id,
        current_user.id,
        session,
    )
    if product is None:
        raise_product_not_found()

    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    data: ProductUpdate,
    current_user: CurrentUser,
    session: SessionDep,
):
    product = product_service.update_product(
        product_id,
        data,
        current_user.id,
        session,
    )
    if product is None:
        raise_product_not_found()

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: CurrentUser,
    session: SessionDep,
):
    deleted = product_service.delete_product(
        product_id,
        current_user.id,
        session,
    )
    if not deleted:
        raise_product_not_found()

    return Response(status_code=status.HTTP_204_NO_CONTENT)