from sqlmodel import select

from models.product import Product
from schemas.product import ProductCreate, ProductUpdate


def create_product(data: ProductCreate, user_id: int, session):
    product = Product(**data.model_dump(), user_id=user_id)
    session.add(product)
    session.commit()
    session.refresh(product)

    return product


def get_products(user_id: int, session):
    return session.exec(
        select(Product).where(Product.user_id == user_id)
    ).all()


def get_product(product_id: int, user_id: int, session):
    return session.exec(
        select(Product).where(
            Product.id == product_id,
            Product.user_id == user_id,
        )
    ).first()


def update_product(product_id: int, data: ProductUpdate, user_id: int, session):
    product = get_product(product_id, user_id, session)
    if product is None:
        return None

    product_data = data.model_dump(exclude_unset=True)
    product.sqlmodel_update(product_data)
    session.add(product)
    session.commit()
    session.refresh(product)

    return product


def delete_product(product_id: int, user_id: int, session):
    product = get_product(product_id, user_id, session)
    if product is None:
        return False

    session.delete(product)
    session.commit()

    return True