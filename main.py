from fastapi import FastAPI

from controller.auth_controller import router as auth_router
from controller.product_controller import router as product_router
from db.database import create_tables
from models.product import Product
from models.user import User

app = FastAPI(lifespan=create_tables)

app.include_router(auth_router)
app.include_router(product_router)
