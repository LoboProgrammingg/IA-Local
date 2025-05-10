from pydantic import BaseModel

from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.types import Send

from schemas import *
from prompts import *

from dotenv import load_dotenv
load_dotenv()

llm = ChatOllama(model="llama3.1:8b-instruct-q4_K_S")
reasoning_llm = ChatOllama(model="deepseek-r1:8b")


def build_first_queries(state: ReportState):
    
    user_input = state.user_input
    
    prompt = build_queries.format(user_input=user_input)
    
    return {""}


builder = StateGraph(ReportState)

graph = builder.compile

if __name__ == "__main__":
    user_input = """
    Can you explain to me how is the full process of building an LLM? from scratching to deployment.
    """
    graph.invoke({"user_input": user_input})
