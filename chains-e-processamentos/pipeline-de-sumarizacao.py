from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

template_summary = PromptTemplate(
    input_variables=["text"],
    template="Resuma o seguinte texto de forma concisa:\n\n{text}"
)

# Criação da pipeline (chain) utilizando a sintaxe mais recente do LCEL
chain = template_summary | llm | StrOutputParser()

long_text = """
LangChain é um framework para desenvolvimento de aplicações com modelos de linguagem.
Ele fornece ferramentas para criar chains, agentes e memória de conversação.
Com LangChain é possível conectar LLMs a fontes de dados externas, APIs e ferramentas.
O framework suporta vários provedores de modelos como OpenAI, Anthropic, Google e outros.
LangChain facilita a criação de pipelines complexos de processamento de linguagem natural.
"""

splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=70)
parts = splitter.create_documents([long_text])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
map_prompt = PromptTemplate.from_template("Write a concise summary of the following text:\n\n{context}")
map_chain = chain | llm | StrOutputParser()

prepare_map_chain = RunnableLambda(lambda docs: [{"context": doc.page_content} for doc in docs])
map_stage = prepare_map_chain | map_chain.map()

reduce_prompt = PromptTemplate.from_template("Write a concise summary of the following text:\n\n{context}")
reduce_chain = chain | llm | StrOutputParser()
prepare_reduce_input = RunnableLambda(lambda summaries: {"context": "\n\n".join(summaries)})
pipeline = map_stage | prepare_reduce_input | reduce_chain

result = pipeline.invoke(parts)
print(result)