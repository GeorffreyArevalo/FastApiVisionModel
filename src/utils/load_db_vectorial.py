import os

from langchain.embeddings import HuggingFaceEmbeddings
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
            pc = Pinecone( api_key=envs()['API_KEY_PINECONE'] )
            VectorialDB.INDEX_NAME = envs()['INDEX_NAME_PINECONE']
            # model_id_embeddings = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
            model_id_embeddings = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
            VectorialDB.embeddings = HuggingFaceEmbeddings( model_name=model_id_embeddings )
            VectorialDB.vstore = PineconeVectorStore.from_existing_index(VectorialDB.INDEX_NAME, VectorialDB.embeddings)
        return [VectorialDB.vstore, VectorialDB.embeddings, VectorialDB.INDEX_NAME]
            
            

