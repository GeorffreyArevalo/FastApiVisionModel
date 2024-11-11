import cloudinary
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from huggingface_hub import login

from src.utils.get_envs import envs
from src.utils.load_db_vectorial import VectorialDB
from src.utils.load_model import ModelProcessor


class Server:
    def __init__(self, routes: APIRouter) -> None:
        self.__app = FastAPI()
        self.routes = routes
        
    def config(self):
        load_dotenv()
        cloudinary.config(
            cloud_name = envs()['CLOUDINARY_NAME'],
            api_key = envs()['CLOUDINARY_API_KEY'],
            api_secret = envs()['CLOUDINARY_API_SECRET'],
            secure = True
        )
        login( token=envs()['HUGGING_FACE_TOKEN'] )
        
    def load_models(self):
        ModelProcessor.get_model_processor()
        ModelProcessor.get_model_translate()
        VectorialDB.get_db_vectorial()
        
    def start(self):
        self.config()
        self.load_models()
        self.__app.include_router(self.routes)
        return self.__app





