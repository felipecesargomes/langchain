from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
question_template = PromptTemplate.from_template(
    "Answer the following question in Portuguese:\n ```{question}```"
)

chain = question_template | llm

result = chain.invoke({"question": "O que é Langchain?"})
print(result)
