from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from pinecone import Pinecone, ServerlessSpec 
from pymongo import MongoClient
import os 
from dotenv import load_dotenv 
from langchain_pinecone import PineconeVectorStore 
from uuid import uuid4


load_dotenv()


def initialize_vector_store():
    pc = Pinecone()
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    index_name = 'professores-agil'
    index = pc.Index(name=index_name)
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    vector_store = PineconeVectorStore(index, embeddings)
    return vector_store