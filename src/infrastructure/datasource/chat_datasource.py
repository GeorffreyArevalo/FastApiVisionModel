
import requests
from cloudinary.uploader import upload
from fastapi import UploadFile
from PIL import Image
from sqlalchemy.orm import Session

from src.data.models.chat_model import ChatModel
from src.utils.load_db_vectorial import VectorialDB
from src.utils.load_model import ModelProcessor
import copy

class ChatDataSource:
        
    @staticmethod
    def send_message( db: Session, question: str, image: UploadFile | None, id_chat: int | None, id_user: int):
        
        if id_chat is None:
            id_chat = ChatDataSource.save_chat( db=db, title=question, id_user=id_user )
        
        [messages_db, url_image_db] = ChatDataSource.get_memory_model(image, id_chat, question)
        
        url_image = ''
        if image:
            print('==============> Imagen en el Data Sources')
            print(f'Image is None: {image.size}')
            image_content = image.file
            upload_result = upload(image_content, folder='chat')
            url_image = upload_result['secure_url']

        image_pillow = None
        if url_image_db:
            image_pillow = Image.open( requests.get(url_image_db, stream=True).raw )
        
        if image:
            image_pillow = Image.open( image.file )
                
        response = ChatDataSource.get_response_model( question, image_pillow, messages_db, image is not None )
        
        response_split = response.split('<|start_header_id|>assistant<|end_header_id|>\n\n')[-1].split('<|eot_id|>')[0]
        
        ChatDataSource.save_data_db_vectorial( url_image=url_image, question=question, response_split=response_split, id_chat=id_chat )
        
        return {
            "question": question,
            "answer": response_split
        }
        
        
    @staticmethod
    def get_memory_model(image: str | None, id_chat: int, question: str):
        [ vstore, *_ ] = VectorialDB.get_db_vectorial()

        messages_vectorial = vstore.similarity_search( filter={'id_chat': id_chat}, query=question, k=10 )
        messages_vectorial_images = vstore.similarity_search( filter={ "image": {"$exists": True, "$ne": ""} }, query='' )
        
        message_image = None
        messages = []
        url_image = None
        
        if image is None:
            message_image = messages_vectorial_images[-1] if len( messages_vectorial_images ) > 0 else None
            messages.append({
                'role': message_image.metadata['role'],
                'content': [
                    {"type": "image"},
                    {"type": "text", "text": message_image.page_content}
                ]
            })
            
            url_image = message_image.metadata['image']
        
        for message_data in messages_vectorial:
            messages.append({
                'role': message_data.metadata['role'],
                'content': [
                    {"type": "text", "text": message_data.page_content}
                ]
            })
        
        return [messages, url_image]
    
        
    @staticmethod
    def save_data_db_vectorial( url_image: str, question: str, response_split: str, id_chat: int):
        [ vstore, embeddings, INDEX_NAME ] = VectorialDB.get_db_vectorial()
        
        vstore.from_texts(
            texts=[question, response_split], embeddings=embeddings,
            metadatas=[
                {'role': 'user', 'id_chat': id_chat, 'image': url_image},
                {'role': 'assistant', 'id_chat': id_chat}
            ], index_name=INDEX_NAME
        )
        
    @staticmethod
    def save_chat( db: Session, title: str | None, id_user: int ):
        chat_db = ChatModel( title=title, user_id=id_user )
        db.add( chat_db )
        db.commit()
        db.refresh( chat_db )
        return chat_db.id
        
    @staticmethod
    def get_response_model( question: str, image: Image, messages: list, has_image: bool ):
        [model, processor] = ModelProcessor.get_model_processor()
        
        if has_image:
            messages.append([
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
            ])
        else:
            messages.append([
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        },
                    ]
                }
            ])
            
        
        input_text = processor.apply_chat_template( messages, add_generation_prompt=True )
        
        inputs = processor(
            image,
            input_text,
            add_special_tokens=False,
            return_tensors="pt"
        ).to(model.device)
        
        output = model.generate(**inputs, max_new_tokens=1000)
        
        return processor.decode(output[0])
        
