import os

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from src.utils.get_envs import envs


class VectorialDB:
    vstore = None
    INDEX_NAME = None
    embeddings = None
    
    @staticmethod
    def get_db_vectorial():
        if VectorialDB.vstore is None:
            os.environ['PINECONE_API_KEY'] = envs()['API_KEY_PINECONE']
            os.environ['OPENAI_API_KEY'] = envs()['OPENAI_KEY']
            pc = Pinecone( api_key=envs()['API_KEY_PINECONE'] )
            VectorialDB.INDEX_NAME = envs()['INDEX_NAME_PINECONE']
            model_id_embeddings = 'text-embedding-3-small'
            VectorialDB.embeddings = OpenAIEmbeddings( model=model_id_embeddings )
            VectorialDB.vstore = PineconeVectorStore.from_existing_index(VectorialDB.INDEX_NAME, VectorialDB.embeddings)
        return [VectorialDB.vstore, VectorialDB.embeddings, VectorialDB.INDEX_NAME]
            
            

