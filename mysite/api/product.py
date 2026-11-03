from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import SessionLocal
from mysite.database.models import Product
from mysite.schemas.product_schema import ProductInputSchema, ProductOutputSchema
from typing import List


product_router = APIRouter(prefix="/products", tags=["Products"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post("/", response_model=ProductOutputSchema)
async def product_create(product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get("/", response_model=list[ProductOutputSchema])
def product_list(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get("/{product_id}/", response_model=ProductOutputSchema)
async def product_detail(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Мындай товар жок', status_code=400)

    return product_db


@product_router.put('/{order_id}/', response_model=dict)
async def product_update(product_id: int, product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Мындай товар жок', status_code=400)

    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, [product_value])

    db.commit()
    db.refresh(product_db)
    return {'message': 'Маалыматтар озгорулду'}


@product_router.delete(f"/{'product_id'}/", response_model=dict)
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Мындай товар жок', status_code=400)

    db.delete(product_db)
    db.commit()
    return {'message': 'Товар очурулду'}
