# -*- coding: utf-8 -*-
import time
from fastapi import Request
from starlette.responses import Response
from services.master.logger import logger
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class LoggerMiddleware(BaseHTTPMiddleware):

    # https://fastapi.tiangolo.com/zh/tutorial/middleware/
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = int(time.time() * 1000)
        response = await call_next(request)
        end_time = int(time.time() * 1000)
        logger.info(
            f"{request.method} | {request.url.path} | {request.client.host} | status code :{response.status_code} | "
            f"耗时: {(end_time - start_time) / 1000}s")
        return response


middlewares = [
    # 日志中间件
    Middleware(LoggerMiddleware)
]
