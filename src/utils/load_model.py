

import torch
from transformers import AutoProcessor, MllamaForConditionalGeneration


class ModelProcessor:
    
    model = None
    processor = None
       
    @staticmethod
    def get_model_processor():
        
        if ModelProcessor.model is None:
            model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
            
            ModelProcessor.model = MllamaForConditionalGeneration.from_pretrained(
                model_id,
                torch_dtype=torch.bfloat16,
                device_map="auto"
            )
            
            ModelProcessor.processor = AutoProcessor.from_pretrained(model_id)
        
        return [ModelProcessor.model, ModelProcessor.processor]
    








