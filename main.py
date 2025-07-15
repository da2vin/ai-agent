#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import datetime
from typing import Annotated

from dotenv import load_dotenv
from langgraph.prebuilt.chat_agent_executor import AgentState

from utils.logger import get_logger
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv(verbose=True)

logger = get_logger("hami")


class CustomState(AgentState):
    user_id: str


@tool(return_direct=True)
def get_user_info(
        state: Annotated[CustomState, InjectedState]
) -> str:
    """
    查询用户信息
    :param state:
    :return:
    """
    user_id = state['user_id']
    return f"{user_id}用户的姓名：da2vin，年龄：33"


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
    tools=[get_current_date, get_user_info],
    state_schema=CustomState,
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
                "messages": messages,
                "user_id": "user_123",
            },
            config)
        print(f"assistant: {result['messages'][-1].content}\n")


if __name__ == '__main__':
    main()
