# 读取markdown内容
from langchain.text_splitter import MarkdownHeaderTextSplitter
# from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import numpy as np


def get_embedding():
    model_name = "BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )


content_path = r"../data/vtk_code.md"
with open(content_path, "r") as f:
    page_content = f.read()

markdown_document = page_content

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

# 假设 headers_to_split_on 已经定义
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(markdown_document)

# 初始化嵌入模型
# embeddings = FastEmbedEmbeddings(cache_dir='../data/cache')

# 创建一个空列表来存储文档和它们的元数据
documents = []

for i, doc in enumerate(md_header_splits):
    documents.append(doc)

embeddings=get_embedding()

db = FAISS.from_documents(documents, embeddings)

db.save_local("../data/faiss_cache")