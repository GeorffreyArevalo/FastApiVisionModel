from openai import OpenAI

from src.utils.get_envs import envs


class ModelProcessor:
    
    client=None
    translate=None
    
    @staticmethod
    def get_model_processor():
        
        if ModelProcessor.client is None:
            ModelProcessor.client = OpenAI(api_key=envs()['OPENAI_KEY'])
            
        return ModelProcessor.client
    








