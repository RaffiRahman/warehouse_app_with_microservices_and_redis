from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import get_redis_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)
