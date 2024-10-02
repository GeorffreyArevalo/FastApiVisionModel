
from cloudinary.uploader import upload
from fastapi import UploadFile
from PIL import Image
from sqlalchemy.orm import Session

from src.utils.load_model import ModelProcessor


class ChatDataSource:
    
    @staticmethod
    def send_message( db: Session, question: str, image: UploadFile):
            
        [model, processor] = ModelProcessor.get_model_processor()
        
        image = Image.open( image.file )
        
        print(f'Image Pillow {image}')
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {
                        "type": "text",
                        "text": question
                    },
                ]
            }
        ]
        
        input_text = processor.apply_chat_template( messages, add_generation_prompt=True )
        inputs = processor(
            image,
            input_text,
            add_special_tokens=False,
            return_tensors="pt"
        ).to(model.device)
        
        output = model.generate(**inputs, max_new_tokens=30)
        
        # if image:
        #     upload_result = upload(image.file, folder='chat')
        #     url = upload_result['secure_url']
            
        print(output[0])
        
        return {
            "question": question,
            "answer": processor.decode(output[0])
        }
        
        
        
        
        
        
        
    









