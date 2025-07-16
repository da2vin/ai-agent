#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import add
from typing import Annotated, Literal
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph, MessagesState
from langgraph.types import interrupt, Command

from utils.logger import get_logger
from typing_extensions import TypedDict

load_dotenv()

logger = get_logger("demo02")

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add]


def human_approval(state: State) -> Command[Literal["call_llm", END]]:
    is_approved = interrupt(
        {
            "question": "是否同意继续调用大模型"
        }
    )
    if is_approved:
        return Command(goto="call_llm")
    else:
        return Command(goto="END")


llm = init_chat_model(model="openai:gpt-4o-mini")


def call_llm(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(State)

# builder.add_node("human_approval", human_approval)
# builder.add_node("call_llm", call_llm)
# builder.add_edge(START, "human_approval")

builder.add_node(call_llm, "call_llm")
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}

while True:
    prompt = input("User:")
    messages = [
        HumanMessage(content=prompt)
    ]
    response = graph.invoke({
        "messages": messages
    }, config=config)
    print("assistant:" + response["messages"][-1].content)

# graph_builder = StateGraph(State)
#
# llm = init_chat_model(model="openai:gpt-4o-mini")
#
# memory = MemorySaver()
#
#
# def chatbot(state: State):
#     return {"messages": [llm.invoke(state["messages"])]}
#
#
# # The first argument is the unique node name
# # The second argument is the function or object that will be called whenever
# # the node is used.
# graph_builder.add_node("chatbot", chatbot)
#
# graph_builder.add_edge(START, "chatbot")
#
# graph_builder.add_edge("chatbot", END)
#
# graph = graph_builder.compile(checkpointer=memory)
#
#
# # 保存状态图的可视化表示
# def save_graph_visualization(graph: StateGraph, filename: str = "graph.png") -> None:
#     """保存状态图的可视化表示。
#
#     Args:
#         graph: 状态图实例。
#         filename: 保存文件路径。
#     """
#     # 尝试执行以下代码块
#     try:
#         # 以二进制写模式打开文件
#         with open(filename, "wb") as f:
#             # 将状态图转换为Mermaid格式的PNG并写入文件
#             f.write(graph.get_graph().draw_mermaid_png())
#         # 记录保存成功的日志
#         logger.info(f"Graph visualization saved as {filename}")
#     # 捕获IO错误
#     except IOError as e:
#         # 记录警告日志
#         logger.warning(f"Failed to save graph visualization: {e}")
#
#
# save_graph_visualization(graph)
#
# config = {"configurable": {"thread_id": "1"}}
#
#
# def stream_graph_updates(user_input: str):
#     for event in graph.stream({"messages": [{"role": "user", "content": user_input}]},
#                               config):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)
#
#
# while True:
#     try:
#         user_input = input("User: ")
#         if user_input.lower() in ["quit", "exit", "q"]:
#             print("Goodbye!")
#             break
#         stream_graph_updates(user_input)
#     except:
#         # fallback if input() is not available
#         user_input = "What do you know about LangGraph?"
#         print("User: " + user_input)
#         stream_graph_updates(user_input)
#         break
