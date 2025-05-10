from pydantic import BaseModel

from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.types import Send

from tavily import TavilyClient

from schemas import *
from prompts import *

from dotenv import load_dotenv
load_dotenv()

llm = ChatOllama(model="llama3.1:8b-instruct-q4_K_S")
reasoning_llm = ChatOllama(model="deepseek-r1:8b")


def build_first_queries(state: ReportState):
    class QueryList(BaseModel):
        queries: List[str]
    
    user_input = state.user_input
    
    prompt = build_queries.format(user_input=user_input)
    query_llm = llm.with_structured_output(QueryList)
    
    result = query_llm.invoke(prompt)
    
    return {"queries": result.queries}


def spawn_researchers(state: ReportState):
    return [Send('single_search', query)
            for query in state.queries]


def single_search(query: str):
    query = results.queries[0]
    tavily_client = TavilyClient()
    
    results = tavily_client.search(query,
                                   max_results=1,
                                   include_raw_content=False
                                   )
    
    url = results["results"][0]["url"]
    url_extraction = tavily_client.extract(url)
    
    if len(url_extraction["results"]) > 0:
        raw_content = url_extraction["results"][0]["raw_content"]
        prompt = resume_search.format(user_input=user_input,
                                      search_results=raw_content)
        llm_result = llm.invoke(prompt)
        
        query_results = QueryResult(title=results["results"][0]["title"],
                                    url=url,
                                    resume=llm_result.content)

    return {'query_results': [query_results]}



builder = StateGraph(ReportState)

graph = builder.compile

if __name__ == "__main__":
    user_input = """
    Can you explain to me how is the full process of building an LLM? from scratching to deployment.
    """
    graph.invoke({"user_input": user_input})
