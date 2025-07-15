#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from utils.logger import get_logger

AB_MODULE = os.getenv("AB_MODULE", default="master")

logger = get_logger(AB_MODULE)
