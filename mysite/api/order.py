from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.models import Order
from mysite.schemas.order_schema import OrderInputSchema, OrderOutputSchema
from mysite.database.db import SessionLocal
from typing import List

order_router = APIRouter(prefix="/order", tags=["Order CRUD"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@order_router.post("/", response_model=OrderOutputSchema)
async def order_create(order: OrderInputSchema, db: Session = Depends(get_db)):
    order_db = Order(**order.dict())
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.get("/", response_model=list[OrderOutputSchema])
async def order_list(db: Session = Depends(get_db)):
    return db.query(Order).all()


@order_router.get("/{order_id}/", response_model=OrderOutputSchema)
async def order_detail(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(detail='Мындай заказ жок', status_code=400)

    return order_db


@order_router.put('/{order_id}/', response_model=dict)
async def order_update(order_id: int, order: OrderInputSchema, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(detail='Мындай заказ жок', status_code=400)

    for order_key, order_value in order.dict().items():
        setattr(order_db, order_key, order_value)

    db.commit()
    db.refresh(order_db)
    return {'message': 'Заказ озгорулду'}


@order_router.delete("/{order_id}/", response_model=dict)
async def order_delete(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(detail='Мындай заказ жок', status_code=400)

    db.delete(order_db)
    db.commit()
    return {'message': 'Заказ очурулду'}
