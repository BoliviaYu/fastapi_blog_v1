import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.db.base import Base
# import models
from app.db.session import engine

import uvicorn


app = FastAPI(title="Fastapi Blog Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
