

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import VERCEL_URL
from .routes import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[F"https://{VERCEL_URL}/",
                   "http://localhost:8000/",
                   "http://127.0.0.1:8000/"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)