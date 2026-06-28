from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import chain
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

question_template = PromptTemplate(
    input_variables=["name"],
    template="Olá, eu sou {name}! Conte uma poesia em português com meu nome!"
)

chain = question_template | llm
result = chain.invoke({"name": "Felipe"})
print(result.content)