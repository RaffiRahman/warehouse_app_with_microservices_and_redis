from fastapi import FastAPI
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

class Product(HashModel):
    name: str
    price: float
    quantity: int
    class Meta:
        database = redis
        model_config = {"arbitrary_types_allowed": True}

@app.post('/product')
def create(product: Product):
    return product.save()

@app.get('/product/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.get('/products')
def get_all():
    # return Product.all_pks()
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.delete('/product/{pk}')
def delete(pk :str):
    return Product.delete(pk)
    