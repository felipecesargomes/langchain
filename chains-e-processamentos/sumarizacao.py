from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
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

# A abordagem "stuff" simplesmente agrupa todo o conteúdo em uma String.
# Podemos simular o mesmo comportamento de 'load_summarize_chain' assim:
combined_text = "\n\n".join(doc.page_content for doc in parts)

# Invocando a chain com o texto consolidado
result = chain.invoke({"text": combined_text})

print(result)