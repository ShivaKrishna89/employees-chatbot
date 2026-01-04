from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from routes.chat import chat


app = FastAPI()
app.include_router(chat)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


