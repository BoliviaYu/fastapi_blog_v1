import sys, os
import time

# add parent_path which is /backend to sys.path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from contextlib import asynccontextmanager
from loguru import logger

# init db
from app.db import engine
from app.db import Base
from app import models

Base.metadata.create_all(bind=engine)

from app.routers import users

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.add(
        "backend/logs/requests_{time}.log",
        rotation="1 week",
        level="INFO",
        compression="zip",
        retention=10,
    )
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")
    logger.remove(handler_id=None)


app = FastAPI(title="Fastapi Blog Backend", lifespan=lifespan)
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        "Request: {method} {url} {status} {process_time:.2f}ms",
        method=request.method,
        url=request.url,
        status=response.status_code,
        process_time=process_time * 1000,
    )

    return response


app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config="backend/app/uvicorn_config.json",
    )
