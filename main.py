from fastapi import FastAPI
import uvicorn
from mysite.api import auth, order, product, ai
from mysite.admin.setup import setup_admin


delivery_app = FastAPI(title='Delivery Service')
delivery_app.include_router(auth.auth_router)
delivery_app.include_router(product.product_router)
delivery_app.include_router(order.order_router)
delivery_app.include_router(ai.ai_router)
setup_admin(delivery_app)



if __name__ == '__main__':
    uvicorn.run(delivery_app, host='127.0.0.1', port=8000)
