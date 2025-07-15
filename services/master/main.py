#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from services.master.logger import logger
from services.master.core.servers import master_server


def create_app():
    ab_module = os.getenv("AB_MODULE", default="master")

    # AB_MODULE环境变量为master时,启动master主服务
    if ab_module == "master":
        logger.info(f"加载 {ab_module} ...")
        return master_server.InitializeApp()
    else:
        raise RuntimeError(f"AB_MODULE can only be master.")


app = create_app()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='services.master.main:app',
        host="0.0.0.0",
        port=4396,
        reload=True,
        workers=1
    )
