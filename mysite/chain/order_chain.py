from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


from mysite.schemas.ai_schema import OrderExtractSchema

llm = ChatOllama(model="llama3.2:latest", temperature=0)
structured_llm = llm.with_structured_output(OrderExtractSchema)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Ты оператор службы доставки. Из сообщения клиента извлеки данные заказа. "
     "Клиент может заказать любой товар. Игнорируй приветствия. "
     "title это только название товара без слов 'заказ' и 'нужен', например: Ноутбук Lenovo. "
     "category это категория товара, например: Электроника, Одежда, Еда, Мебель. "
     "Если количество не указано, quantity = 1. "
     "Если клиент назвал цену, price = эта цена за одну штуку. "
     "Если цену не назвал, price = реалистичная средняя цена одного такого товара в сомах. "
     "price никогда не должен быть 0. "
     "description это краткое описание заказа на русском языке.\n\n"
     "Пример 1: 'Хочу 2 футболки красного цвета'. "
     "title=Футболка, category=Одежда, price=800, quantity=2, description=Две футболки красного цвета.\n"
     "Пример 2: 'Нужен ноутбук Lenovo за 45000'. "
     "title=Ноутбук Lenovo, category=Электроника, price=45000, quantity=1, description=Ноутбук Lenovo."),
    ("human", "{text}"),
])

order_chain = prompt | structured_llm
