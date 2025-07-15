# _*_ coding: utf-8 _*_
from fastapi import APIRouter
from services.master.api.v1 import ping


class MasterApiRouter(object):
    """
    注册路由
    """

    def __new__(cls, *args, **kwargs):
        router = APIRouter(prefix="/api/v1")
        router.include_router(ping.router)
        return router
