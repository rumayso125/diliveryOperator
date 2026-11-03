from email.policy import default

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from .db import Base
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Date
from datetime import date, datetime
from typing import Optional, List
from enum import Enum as PyEnem



class OrderStatusChoices(str, PyEnem):
    pending = "pending"
    confirmed = "confirmed"
    cancel = "cancel"
    delivered = "delivered"


class UserProfile(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String)
    registered_date: Mapped[date] = mapped_column(Date, default=date.today)

    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user', cascade='all, delete-orphan')
    user_order: Mapped[List['Order']] = relationship(back_populates='user', cascade='all, delete-orphan')


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates=('user_token'))


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(50))
    store: Mapped[str] = mapped_column(String(50))
    product_name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product_order: Mapped[List['Order']] = relationship(back_populates='product', cascade='all, delete-orphan')


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement= True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    order_status: Mapped[OrderStatusChoices] = mapped_column(Enum(OrderStatusChoices), default=OrderStatusChoices.pending)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product: Mapped[Product] = relationship(Product, back_populates='product_order')
    user: Mapped[UserProfile] = relationship(back_populates='user_order')
