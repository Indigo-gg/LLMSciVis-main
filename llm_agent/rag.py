import json

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
# from RAG.embedding import get_embedding
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import app_config
import requests

def get_embedding():
    model_name = "BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

'''
根据模型、用户输入和modal返回数据
'''

faiss_db='../data/faiss_cache/index.faiss'
def get_message(user_input, modal, system):
    model = OllamaLLM(base_url=app_config.ollama_url, model=modal)
    template = """Question: {question}
    system:{system}.
    Answer: 请用中文回答我的问题.
    Context:{context}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    new_db = FAISS.load_local(faiss_db, get_embedding())
    docs = new_db.similarity_search(user_input)
    print('相似度检索得到的结果', docs)
    context = docs[0]
    response = chain.invoke({"question": user_input, "system": system, "context": {context}})
    print(response)

# get_message('你好', 'llama3.2:1b', '你是科学可视化专家')
