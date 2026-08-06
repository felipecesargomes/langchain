from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

@tool("calculator", return_direct=True)
def calculator(expression: str) -> str:
    """Avalia uma expressao matematica simples e retorna o resultado."""
    try:
        result = eval(expression)
    except Exception as e:
        return f"Erro: {e}"
    return str(result)

@tool("web_search_mock")
def web_search_mock(query: str) -> str:
    """Ferramenta simulada de busca. Retorna um resultado fixo."""

    data = {
        "Brasil": "Brasilia",
        "Franca": "Paris",
        "Alemanha": "Berlim",
        "Italia": "Roma",
        "Japao": "Toquio",
        "Estados Unidos": "Washington, D.C.",
    }

    for country, capital in data.items():
        if country.lower() in query.lower():
            return f"A capital de {country} e {capital}."
    return "Nao sei a capital desse pais."

# Temperatura baixa deixa as respostas mais consistentes para o parser ReAct.
llm = ChatOpenAI(model_name="gpt-4", disable_streaming=True, temperature=0)
tools = [calculator, web_search_mock]

prompt = PromptTemplate.from_template(
    """
    Responda as perguntas a seguir da melhor forma que puder. Voce tem acesso as seguintes ferramentas.
    Use apenas as informacoes obtidas pelas ferramentas, mesmo que voce saiba a resposta.
    Se a informacao nao for fornecida pelas ferramentas, diga que nao sabe.

    {tools}

    Use o seguinte formato:
    Question: a pergunta de entrada que voce deve responder
    Thought: voce deve sempre pensar no que fazer
    Action: a acao a executar, deve ser uma entre [{tool_names}]
    Action Input: a entrada da acao
    Observation: o resultado da acao
    ... (este Thought/Action/Action Input/Observation pode se repetir N vezes)
    Thought: agora eu sei a resposta final
    Final Answer: a resposta final para a pergunta original

    Regras:
    - Responda SOMENTE em formato ReAct. Nao escreva frases soltas fora do formato.
    - Em cada passo, responda com Thought + Action + Action Input OU com Thought + Final Answer.
    - Se voce escolher uma Action, NAO inclua Final Answer no mesmo passo.
    - Depois de Action e Action Input, pare e aguarde a Observation.
    - Nunca pesquise na internet. Use apenas as ferramentas fornecidas.
    - Se a Observation indicar que nao sabe, a Final Answer deve dizer claramente que nao sabe.

    Exemplo valido de passo com ferramenta:
    Thought: preciso calcular.
    Action: calculator
    Action Input: 10 + 10

    Exemplo valido de resposta final:
    Thought: agora eu sei a resposta final.
    Final Answer: 20

    Comece!

    Question: {input}
    Thought: {agent_scratchpad}"""
)

agent_chain = create_react_agent(llm, tools, prompt=prompt)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent_chain,
    tools=tools,
    verbose=True,
    # Permite recuperar a execucao quando o modelo sair do formato esperado.
    handle_parsing_errors="Formato invalido. Forneca uma Action e Action Input validos, ou forneca um Final Answer.",
    max_iterations=3,
)


response = agent_executor.invoke({"input": "Quanto é 10 + 10 ?"})
print(response.get("output", response))

response_country = agent_executor.invoke({"input": "Qual é a capital do Iran ?"})
print(response_country.get("output", response_country))

response_best_player = agent_executor.invoke({"input": "Qual o melhor jogador da história do Brasil ?"})
print(response_best_player.get("output", response_best_player))