

import torch
from transformers import (
    AutoProcessor,
    BitsAndBytesConfig,
    MllamaForConditionalGeneration,
)


class ModelProcessor:
    
    model = None
    processor = None
       
    @staticmethod
    def get_model_processor():
        
        if ModelProcessor.model is None:
            
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            
            model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
            
            ModelProcessor.model = MllamaForConditionalGeneration.from_pretrained(
                model_id,
                quantization_config=bnb_config
            )
            
            ModelProcessor.processor = AutoProcessor.from_pretrained(model_id)
        
        return [ModelProcessor.model, ModelProcessor.processor]
    








