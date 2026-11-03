from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama

from mysite.config import OLLAMA_URL, OLLAMA_MODEL


answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'Ты готовишь текст ответа клиенту службы доставки. '
            'Ответ должен быть вежливым, на русском языке, в 2-3 предложениях. '
            'Используй обращение клиента только для понимания вопроса. '
            'Не представляй утверждения клиента как проверенные факты. '
            'Не придумывай сроки, причины задержки, возвраты и компенсации. '
            'Не утверждай, что сотрудники уже выполнили действие, '
            'если этого нет в сведениях оператора. '
            'Если нужных сведений нет, сообщи, что информация требует уточнения, '
            'без обещания сроков. '
            'Верни только текст ответа клиенту, без пояснений и рассуждений.'
        ),
        (
            'human',
            'Обращение клиента: {text}\n'
            'Сведения оператора: {facts}'
        ),
    ]
)


answer_model = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0,
    num_predict=1024,                 # было 250, не хватало
    reasoning=False,                  # отключает thinking у reasoning-моделей
    client_kwargs={"timeout": 60},    # не ждать 2 минуты
)


def check_answer(response: AIMessage) -> AIMessage:
    if response.response_metadata.get('done_reason') == 'length':
        raise ValueError('Ответ модели обрезан лимитом num_predict')

    if not str(response.content).strip():
        raise ValueError('Модель вернула пустой ответ')

    return response


answer_chain = (
    answer_prompt
    | answer_model
    | RunnableLambda(check_answer)
    | StrOutputParser()
)