# from langchain.llms import Ollama
from langchain_ollama import OllamaLLM

model = OllamaLLM(base_url='http://localhost:11435',model="llama3.2:1b")
r=model.invoke("请你提出10个手机的品牌")
print(r)