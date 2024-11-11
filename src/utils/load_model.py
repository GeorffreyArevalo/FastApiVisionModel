from openai import OpenAI
from transformers import pipeline

from src.utils.get_envs import envs


class ModelProcessor:
    
    client=None
    translate=None
    
    @staticmethod
    def get_model_processor():
        
        if ModelProcessor.client is None:
            ModelProcessor.client = OpenAI(api_key=envs()['OPENAI_KEY'])
            
        return ModelProcessor.client
    
    @staticmethod
    def get_model_translate():
        if ModelProcessor.translate is None:
            ModelProcessor.translate = pipeline('translation', model='facebook/m2m100_1.2B')
            
        return ModelProcessor.translate








