#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import datetime
from dotenv import load_dotenv
from utils.logger import get_logger
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
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

checkpointer = InMemorySaver()

config = {
    "configurable": {
        "thread_id": "123"
    }
}

agent = create_react_agent(
    model=llm,
    tools=[get_current_date],
    checkpointer=checkpointer,
    prompt="You are a helpful assistant."
)


# async def invoke():
#     messages = [
#         SystemMessage("你是一个私人助手"),
#         HumanMessage("今天是几月几号？"),
#     ]
#
#     result = await agent.ainvoke({
#         "messages": messages
#     })
#     logger.info(result["messages"][-1].content)

def main():
    while True:
        prompt = input("User:")
        messages = [
            HumanMessage(prompt),
        ]
        result = agent.invoke(
            {
                "messages": messages
            },
            config)
        print(f"assistant: {result['messages'][-1].content}\n")


if __name__ == '__main__':
    main()
