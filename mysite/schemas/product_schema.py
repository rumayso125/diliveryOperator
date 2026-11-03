from pydantic import BaseModel
from datetime import datetime


class ProductInputSchema(BaseModel):
    category: str
    store: str
    product_name: str
    price: str


class ProductOutputSchema(BaseModel):
    id: int
    category: str
    store: str
    product_name: str
    price: int
    created_date: datetime