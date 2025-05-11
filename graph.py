from pydantic import BaseModel
from typing import List, Optional

from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.types import Send

import streamlit as st
import logging
from langchain.prompts import PromptTemplate

from tavily import TavilyClient

from dotenv import load_dotenv
load_dotenv()

# Configuração de logs
logging.basicConfig(level=logging.DEBUG)

llm = ChatOllama(model="llama3.1:8b-instruct-q4_K_S")
reasoning_llm = ChatOllama(model="deepseek-r1:8b")

class QueryResult(BaseModel):
    title: str
    url: str
    resume: str

class ReportState(BaseModel):
    user_input: str
    queries: Optional[List[str]] = None
    queries_result: Optional[List[QueryResult]] = None
    final_response: Optional[str] = None

build_queries = PromptTemplate.from_template("""Você é um especialista em gerar perguntas de pesquisa relevantes com base na entrada do usuário. Gere até 3 perguntas de pesquisa para investigar a seguinte entrada do usuário: "{user_input}"
Formate sua resposta como uma lista de strings.""")

resume_search = PromptTemplate.from_template("""Você é um especialista em resumir resultados de pesquisa para responder à pergunta do usuário. Com base nos seguintes resultados da pesquisa: "{search_results}", forneça um resumo conciso e informativo que ajude a responder à pergunta do usuário: "{user_input}".
Mantenha o resumo o mais conciso possível, mas garanta que ele capture os principais pontos das descobertas da pesquisa.""")

build_final_response = PromptTemplate.from_template("""Você é um escritor de relatórios especializado em sintetizar informações de várias fontes. Com base nos seguintes resultados da pesquisa:
{search_results}

e nas seguintes referências:
{references}

gere uma resposta abrangente e bem referenciada à pergunta do usuário: "{user_input}".
Certifique-se de que a resposta seja clara, concisa e cite todas as fontes relevantes usando colchetes ([número]). Inclua uma seção de referências no final da sua resposta.""")

def build_first_queries(state: ReportState):
    class QueryList(BaseModel):
        queries: List[str]

    user_input = state.user_input

    prompt = build_queries.format(user_input=user_input)
    query_llm = llm.with_structured_output(QueryList)

    result = query_llm.invoke(prompt)

    logging.debug(f"Queries geradas: {result.queries}")

    return {"queries": result.queries}

def spawn_researchers(state: ReportState):
    if not state.queries:
        logging.warning("Nenhuma query foi gerada.")
        return []
    return [Send('single_search', {"query": query, "user_input": state.user_input})
            for query in state.queries]

def single_search(data: dict):
    query = data["query"]
    user_input = data["user_input"]
    logging.debug(f"Iniciando pesquisa para a query: {query}")

    tavily_client = TavilyClient()

    results = tavily_client.search(query,
                                   max_results=1,
                                   include_raw_content=False
                                   )

    if results and results["results"]:
        url = results["results"][0]["url"]
        url_extraction = tavily_client.extract(url)

        if url_extraction and len(url_extraction["results"]) > 0:
            raw_content = url_extraction["results"][0]["raw_content"]
            prompt = resume_search.format(user_input=user_input,
                                          search_results=raw_content)
            llm_result = llm.invoke(prompt)

            query_results = QueryResult(title=results["results"][0]["title"],
                                        url=url,
                                        resume=llm_result.content)
            logging.debug(f"Resumo gerado: {query_results}")
            return {'query_results': [query_results]}
    logging.warning(f"Nenhum resultado encontrado para a query: {query}")
    return {'query_results': []}

def final_writer(state: ReportState):
    if not state.queries_result or all(len(result.query_results) == 0 for result in state.queries_result):
        logging.error("Nenhum resultado foi retornado das pesquisas.")
        return {
            "final_response": "Não foi possível gerar uma resposta devido à falta de resultados de pesquisa. "
                              "Tente reformular sua pergunta ou verificar sua conexão com a Internet."
        }

    search_results = ''
    references = ''
    for i, result in enumerate(state.queries_result or []):
        if result.query_results:
            for query_result in result.query_results:
                search_results += f"[{i+1}]\n\n"
                search_results += f'Título: {query_result.title}\n'
                search_results += f'URL: {query_result.url}\n'
                search_results += f'Conteúdo: {query_result.resume}\n'
                search_results += "=====================\n\n"

                references += f"[{i+1}] - [{query_result.title}] ({query_result.url})\n"

    prompt = build_final_response.format(user_input=state.user_input,
                                         search_results=search_results,
                                         references=references)
    llm_result = reasoning_llm.invoke(prompt)
    final_response = llm_result.content + "\n\n" + references

    logging.debug(f"Resposta final gerada: {final_response}")

    return {"final_response": final_response}

builder = StateGraph(ReportState)
builder.add_node("build_first_queries", build_first_queries)
builder.add_node("single_search", single_search)
builder.add_node("final_writer", final_writer)

builder.add_edge(START, "build_first_queries")
builder.add_conditional_edges("build_first_queries",
                              spawn_researchers,
                              ["single_search"],)
builder.add_edge("single_search", "final_writer")
builder.add_edge("final_writer", END)
graph = builder.compile()

if __name__ == "__main__":
    st.title("Local Perplexity")
    user_input = st.text_input("Qual a sua pergunta?",
                               value="Como é o processo de construir um LLM?")

    if st.button("Pesquisar"):
        with st.spinner("Gerando resposta..."):
            for output in graph.stream({"user_input": user_input},
                                       stream_mode="debug"):
                if output["type"] == "task_result":
                    st.write(f"Executando {output['payload']['name']}")
                    st.write(output)
            if "final_response" in output["payload"]["result"][-1][1]:
                response = output["payload"]["result"][-1][1]["final_response"]
                if "</think>" in response:
                    think_str = response.split("</think>")[0]
                    final_response = response.split("</think>")[1]

                    with st.expander("Reflexão", expanded=False):
                        st.write(think_str)
                    st.write(final_response)
                else:
                    st.write(response)
            else:
                st.error("Não foi possível gerar uma resposta final.")