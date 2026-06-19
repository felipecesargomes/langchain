from langchain_core.prompts import PromptTemplate

template = PromptTemplate(input_variable=["name"],template="Hi, I'm {name}! Tell me a joke with my name!")

text = template.format(name="Felipe")
print(text)