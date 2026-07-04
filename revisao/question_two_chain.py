from langchain_core.runnables import chain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

@chain
def square(x) -> dict:
    number = x["x"]
    return {"x": number * number}

template_square = PromptTemplate.from_template(
    "Calculate the square of the following number:\n ```{x}```"
)


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = square | template_square | llm

result = chain.invoke({"x": 16})
print(result)