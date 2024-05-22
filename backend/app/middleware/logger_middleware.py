from loguru import logger

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, header_namespace: str):
        super().__init__(app)
        self.header_namespace = header_namespace

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error("Internal Server Error")
            raise e
        else:
            logger.info(f"{request.method} {request.url} {response.status_code}")

        return response
