# ===================== Importing FastAPI necessary packages =============
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routers.routers import router

import base64
import binascii

from fastapi.middleware.cors import CORSMiddleware
from src.settings import settings
# ------------------ FastAPI variable ----------------------------------
tag_metadata =[
    {
        "name": "user"
    },
    {
        "name":"admin"
    },
    {
        "name":"auth"
    },
]
app  = FastAPI()

# app.mount("/post", StaticFiles(directory="post"), name="post")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
