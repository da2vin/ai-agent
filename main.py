#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv(verbose=True)

llm = ChatOpenAI(model="gpt-4o-mini")


@tool
def get_current_date():
    """
    获取今天的日期
    :return:
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")


agent = create_react_agent(
    model=llm,
    tools=[get_current_date],
    prompt="You are a helpful assistant.",
)

result = agent.invoke({"messages": [
    {"role": "user", "content": "今天是几月几号？"}
]})

print(result)
