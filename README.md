# Local Perplexity

Local Perplexity é uma aplicação que utiliza modelos de linguagem (LLMs) para responder a perguntas complexas de forma estruturada e bem referenciada. Este projeto é ideal para quem busca respostas detalhadas, baseadas em pesquisa e organizadas de maneira clara.

---

## 📋 **Funcionalidades**

1. **Geração de Perguntas de Pesquisa**  
   - Analisa a entrada do usuário e gera até 3 perguntas relevantes para investigação.  

2. **Pesquisa e Resumo**  
   - Realiza buscas em fontes externas confiáveis e gera resumos claros e concisos.  

3. **Geração de Respostas Finais**  
   - Produz uma resposta detalhada e referenciada com base nos resultados obtidos.  

4. **Interface Interativa**  
   - Utiliza Streamlit para oferecer uma experiência simples e intuitiva para o usuário interagir com o sistema.  

---

## 🛠️ **Tecnologias Utilizadas**

### **Bibliotecas e Frameworks**
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Validação e estruturação de dados.
- **[LangChain](https://docs.langchain.com/)**: Criação e manipulação de prompts para modelos de linguagem.
- **[Streamlit](https://streamlit.io/)**: Interface de usuário interativa.
- **[Tavily](https://tavily.com/)**: Realização de buscas e extração automatizada de informações.
- **[dotenv](https://pypi.org/project/python-dotenv/)**: Gerenciamento de variáveis de ambiente.
- **[StateGraph](https://github.com/langgraph/langgraph)**: Gerenciamento do fluxo de estados da aplicação.

### **Modelos de Linguagem**
- **ChatOllama**: Utilizado para geração inicial de perguntas e resposta final.
- **DeepSeek**: Aplicado para raciocínios avançados e refinamento da resposta final.

---

## 🧩 **Arquitetura**

### **1. Fluxo de Estados**
O fluxo é gerenciado por um `StateGraph`, que organiza a execução das tarefas em etapas:

1. **`build_first_queries`**  
   - Gera perguntas de pesquisa com base na entrada do usuário.

2. **`spawn_researchers`**  
   - Cria tarefas para realizar buscas em fontes externas.

3. **`single_search`**  
   - Realiza a busca e resume os resultados encontrados.

4. **`final_writer`**  
   - Compila os resultados e gera uma resposta final detalhada e referenciada.

---

### **2. Prompts Personalizados**
- **Geração de Perguntas**: Cria perguntas relevantes para pesquisa.  
- **Resumo de Resultados**: Resume informações importantes dos resultados encontrados.  
- **Resposta Final**: Gera uma resposta clara, concisa e bem referenciada.  

---

## 🚀 **Como Executar o Projeto**

### **Pré-requisitos**
- Python 3.8 ou superior.
- Instale as dependências do projeto com o seguinte comando:

  ```bash
  pip install -r requirements.txt
  ```

### **Passos para Execução**
1. Crie um arquivo `.env` com as variáveis de ambiente necessárias (como tokens de acesso a APIs externas, por exemplo).
2. Execute o comando abaixo para iniciar a aplicação:

   ```bash
   streamlit run app.py
   ```

3. Acesse a interface no navegador em: `http://localhost:8501`.

---

## 📖 **Exemplo de Uso**

### **Entrada do Usuário**
- Pergunta: _"Como é o processo de construir um LLM?"_

### **Processo**
1. Geração de perguntas de pesquisa relacionadas:
   - "Quais são os passos necessários para construir um LLM?"
   - "Quais ferramentas são usadas no treinamento de LLMs?"
   - "Quais desafios estão envolvidos na construção de LLMs?"

2. Realização das buscas e resumos:
   - Busca em fontes relevantes para obter informações detalhadas.
   - Resumo dos resultados mais importantes.

3. Geração da resposta final:
   - Resposta clara, detalhada e com referências.

### **Saída**
Uma resposta detalhada com referências organizadas, incluindo os links para consulta adicional.

---

## 👥 **Contribuindo**

Contribuições são muito bem-vindas!  
Siga as etapas abaixo para contribuir com o projeto:

1. Faça um fork do repositório.
2. Crie uma branch para suas mudanças:  
   ```bash
   git checkout -b minha-feature
   ```
3. Envie suas alterações:  
   ```bash
   git commit -m "Minha nova funcionalidade"
   git push origin minha-feature
   ```
4. Abra um Pull Request.

---

## 📬 **Contato**

Se você tiver dúvidas, sugestões ou feedback, entre em contato:  
📧 Email: `matheusloboo2001@gmail.com`