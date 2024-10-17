import os

import pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from src.utils.get_envs import envs

from pinecone import Pinecone


class VectorialDB:
    vstore = None
    INDEX_NAME = None
    embeddings = None
    
    @staticmethod
    def get_db_vectorial():
        if VectorialDB.vstore is None:
            os.environ['PINECONE_API_KEY'] = envs()['API_KEY_PINECONE_ENV']
            #pinecone.init( api_key = envs()['API_KEY_PINECONE_ENV'] )
            Pinecone( api_key=envs()['API_KEY_PINECONE_ENV'] )
            VectorialDB.INDEX_NAME = envs()['INDEX_NAME_PINECONE']
            model_id_embeddings = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
            VectorialDB.embeddings = HuggingFaceEmbeddings( model_name=model_id_embeddings )
            VectorialDB.vstore = PineconeVectorStore.from_existing_index(VectorialDB.INDEX_NAME, VectorialDB.embeddings)
        return [VectorialDB.vstore, VectorialDB.embeddings, VectorialDB.INDEX_NAME]
            
            

