# -*- coding: utf-8 -*-
from typing import Any

from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/ping", name="测试接口")
async def ping() -> Any:
    return Response(content="pong")
