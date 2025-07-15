#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import datetime
from dotenv import load_dotenv
from utils.logger import get_logger
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv(verbose=True)

logger = get_logger("hami")


@tool
def get_current_date():
    """
    获取今天的日期
    :return:
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")


llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_react_agent(
    model=llm,
    tools=[get_current_date],
    prompt="You are a helpful assistant.",
)


async def invoke():
    messages = [
        SystemMessage("你是一个私人助手"),
        HumanMessage("今天是几月几号？"),
    ]

    result = await agent.ainvoke({
        "messages": messages
    })
    logger.info(result["messages"][-1].content)


if __name__ == '__main__':
    asyncio.run(invoke())
