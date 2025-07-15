#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.master.router.v1 import master_router
from services.master.core.middlewares.logger_middleware import middlewares


class InitializeApp(object):
    """
    注册App
    """

    def __new__(cls, *args, **kwargs):
        app = FastAPI(title="AI-Backend-MASTER", middleware=middlewares)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*", ],
            allow_credentials=True,  # 允许携带cookie
            allow_methods=["*"],  # 允许的HTTP方法
            allow_headers=["*"],  # 允许的请求头
        )

        cls.event_init(app)
        cls.register_router(app)
        return app

    @staticmethod
    def register_router(app: FastAPI) -> None:
        """
        注册路由
        :param app:
        :return:
        """
        # 项目API
        app.include_router(
            master_router.MasterApiRouter(),
        )

    @staticmethod
    def event_init(app: FastAPI) -> None:
        """
        事件初始化
        :param app:
        :return:
        """

        @app.on_event("startup")
        async def startup():
            pass

        @app.on_event('shutdown')
        async def shutdown():
            """
            关闭
            :return:
            """
            pass
