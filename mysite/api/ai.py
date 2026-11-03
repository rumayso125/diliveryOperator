import asyncio
from fastapi import APIRouter, HTTPException
from mysite.chain.ticket_chain import ticket_chain
from mysite.schemas.ai_schema import TicketInputSchema, TicketOutputSchema, AnswerInputSchema, AnswerOutputSchema
from langchain_core.exceptions import OutputParserException
from mysite.chain.answer_chain import answer_chain
from mysite.chain.order_chain import order_chain
from mysite.schemas.ai_schema import OrderInputSchema, OrderOutputSchema
import re

ai_router = APIRouter(prefix='/ai', tags=['AI Assistant'])


@ai_router.post(path='/analyze/', response_model=TicketOutputSchema)
async def analyze_ticket(ticket: TicketInputSchema):
    text = ticket.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилип жатат')

    try:
        result = await asyncio.wait_for(
            ticket_chain.ainvoke({"text": text}), timeout=120
        )

    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модель тапшырманы аткарганы жетишкен жок')

    except OutputParserException:
        raise HTTPException(status_code=500, detail='Моделдин жообу схемага туура келбейт')

    return result


@ai_router.post(path='/answer/', response_model=AnswerOutputSchema)
async def answer_list(answer: AnswerInputSchema):
    text = answer.text.strip()
    facts = answer.facts.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилип жатат')

    try:
        result = await asyncio.wait_for(
            answer_chain.ainvoke({"text": text, 'facts': facts}), timeout=120
        )

    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модель тапшырманы аткарганы жетишкен жок')

    except OutputParserException:
        raise HTTPException(status_code=500, detail='Моделдин жообу схемага туура келбейт')

    result = result.strip()

    return AnswerOutputSchema(text_draft=result)




def extract_price_from_text(text: str) -> int | None:
    match = re.search(r'(?:за|по|цена|цену)\s*(\d[\d ]*)', text.lower())
    if not match:
        return None
    digits = match.group(1).replace(' ', '')
    return int(digits) if digits else None


@ai_router.post(path='/order/', response_model=OrderOutputSchema)
async def create_order(order: OrderInputSchema):
    text = order.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилип жатат')

    try:
        result = await asyncio.wait_for(
            order_chain.ainvoke({"text": text}), timeout=120
        )

    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модель тапшырманы аткарганы жетишкен жок')

    except OutputParserException:
        raise HTTPException(status_code=500, detail='Моделдин жообу схемага туура келбейт')

    user_price = extract_price_from_text(text)
    price = user_price if user_price else max(result.price, 0)
    quantity = max(result.quantity, 1)

    return OrderOutputSchema(
        title=result.title,
        category=result.category,
        price=price,
        quantity=quantity,
        total_price=price * quantity,
        description=result.description,
    )
