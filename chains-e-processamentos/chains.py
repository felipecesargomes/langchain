from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import chain
from dotenv import load_dotenv
load_dotenv()

@chain
def square(x: int) -> int:
    return {"square_result": x**2}

question_template = PromptTemplate(
    input_variables=["name"],
    template="Olá, eu sou {name}! Conte uma piada em português com meu nome!"
)

question_template2 = PromptTemplate(
    input_variables=["square_result"],
    template="Tell me about the number {square_result}"
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

chain = question_template | model
chain2 = square | question_template2 | model

chain2.invoke({"x": 4})

result = chain.invoke({"name": "Felipe"})
print(result.content)
result2 = square.invoke({"x":10})
print(result2)

