from pydantic import BaseModel, Field


class TicketInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class TicketOutputSchema(BaseModel):
    answer: str = Field(min_length=1, max_length=300)
    order_id: int | None = Field(ge=1, default=None)
    priority: int = Field(ge=1, le=3)



class AnswerInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    facts: str = Field(min_length=1, max_length=1000)


class AnswerOutputSchema(BaseModel):
    text_draft: str
    review: bool = True


class OrderInputSchema(BaseModel):
    text: str


class OrderExtractSchema(BaseModel):
    """Модель клиенттин билдирүүсүнөн ушуну чыгарат"""
    title: str = Field(description="Название товара с заглавной буквы, например: Ноутбук Lenovo")
    category: str = Field(description="Категория товара одним-двумя словами, например: Электроника, Одежда, Еда, Мебель")
    price: int = Field(default=0, description="Цена за одну штуку в сомах, целое число")
    quantity: int = Field(default=1, description="Количество, если не указано то 1")
    description: str = Field(description="Краткое описание заказа на русском языке")

class OrderOutputSchema(BaseModel):
    title: str
    category: str
    price: int
    quantity: int
    total_price: int
    description: str
