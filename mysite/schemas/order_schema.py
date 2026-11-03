from pydantic import BaseModel
from datetime import datetime
from mysite.database.models import OrderStatusChoices


class OrderInputSchema(BaseModel):
    product_id: int
    user_id: int


class OrderOutputSchema(BaseModel):
    id: int
    product_id: int
    user_id: int
    order_status: OrderStatusChoices
    created_date: datetime