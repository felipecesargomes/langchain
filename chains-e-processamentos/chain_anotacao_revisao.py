from langchain_core.runnables import chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

@chain
def square(input: dict) -> dict:
    return {"square_result": input["x"]**2}

template_square = PromptTemplate(
    input_variables=["square_result"],
    template="O resultado do quadrado de um número é {square_result}. Explique esse resultado em texto simples, sem LaTeX ou fórmulas matemáticas."
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

chain_square = square | template_square | llm

result = chain_square.invoke({"x": 5})
print(result.content)
