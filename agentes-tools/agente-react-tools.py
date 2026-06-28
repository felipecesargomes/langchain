from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor, tool, tool
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

@tool("calculator", return_direct=True)
def calculator(expression: str) -> str:
    """Evaluate a simple mathematical expression and return the result as a string."""
    try:
        # Evaluate the expression and return the result
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
    
@tool("web_search_mock")
def web_search_mock(query: str) -> str:
    """Mock function to simulate a web search. Return hardcoded search results for the given query."""
    # In a real implementation, you would perform a web search here.
    data = {"Brazil": "Brasília", "France": "Paris", "Germany": "Berlin"}

    for country, capital in data.items():
        if query.lower() in country.lower():
            return f"The capital of {country} is {capital}."
    return "No results found."

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, disable_streaming=True)
tools = [calculator, web_search_mock]
prompt = PromptTemplate.from_template(
    """
    Answer the following questions as best you can. You have access to the following tools:
    Only use information you get from the tools, even if you know the answer. If you don't know the answer, say "I don't know".
    """
)