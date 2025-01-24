from fastapi import FastAPI, requests
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

redis = get_redis_connection(
    host = 'redis-10298.c264.ap-south-1-1.ec2.redns.redis-cloud.com',
    port = 10298,
    password = 't4rxe5UIKDth1wGapKe3nCytZZ2JxLWh',
    decode_responses = True
)

class ProductOrder(HashModel):
    product_id: str
    quantity: int
    class meta:
        database = redis

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str
    class meta:
        database = redis

@app.post('/orders')
def create(productOrder: ProductOrder):
    req = requests.get(f'http://localhost:8000/product/{productOrder.product_id}')
    product = req.json()
    fee = product['price'] * 0.2

    order = Order(
        product_id = productOrder.product_id,
        price = product['price'],
        fee = fee,
        total = (product['price'] + fee) * productOrder.quantity,
        quantity = productOrder.quantity,
        status = 'pending'
    )

    return order.save()