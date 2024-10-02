import cloudinary
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from huggingface_hub import login

from src.utils.get_envs import envs
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
        
    def load_model(self):
        ModelProcessor.get_model_processor()
        
    def start(self):
        self.config()
        self.load_model()
        self.__app.include_router(self.routes)
        return self.__app




