agent_prompt = """
You are a research planner.

You are working on a project that aims to answer user's questions
using sources found online.

Your answer MUST be technical, using up to date information.
Cite facts, data and specific informations.

Here's the user input:
<USER_INPUT>
{user_input}
</USER_INPUT>
"""

build_queries = agent_prompt + """
Your first objective is to with build a list of queries
that will be used to find answer to the user's question.

Answer with anything between 3-5 queries.
"""