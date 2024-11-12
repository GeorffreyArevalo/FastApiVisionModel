from cloudinary.uploader import upload
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from src.data.models.chat_model import ChatModel
from src.utils.load_db_vectorial import VectorialDB
from src.utils.load_model import ModelProcessor


class ChatDataSource:
    
    
    @staticmethod
    def get_chats_by_user( db: Session, id_user: int ):
        chats = db.query( ChatModel ).filter( ChatModel.user_id == id_user ).all()
        return chats
    
    
    @staticmethod
    def get_messages_by_chat( db: Session, id_chat: int ):
        chat = db.query(ChatModel).filter(ChatModel.id == id_chat).first()
        if chat is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El id del chat no existe.')
        [ vstore, embeddings, INDEX_NAME ] = VectorialDB.get_db_vectorial()
        messages_vectorial = vstore.similarity_search( filter={'id_chat': id_chat}, query='' )
        
        data = []
        
        for message in messages_vectorial:
            data.append({
                "role": message.metadata['role'],
                "content": message.page_content,
                "url_image": message.metadata.get('image'),
            })
            
        return data
        
    
    @staticmethod
    def translate_text(
        text: str,
        lng: str
    ):
        client = ModelProcessor.get_model_processor()
        
        response = client.chat.completions.create(
            model = 'gpt-4o-mini-2024-07-18',
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Traduce el siguiente texto a {lng}: {text}"
                        }
                    ]
                }
            ]
        )
        
        return response.choices[0].message.content
    
        
    @staticmethod
    def send_message( db: Session, question: str, image: UploadFile | None, id_chat: int | None, id_user: int):
        
        if id_chat is None:
            id_chat = ChatDataSource.save_chat( db=db, title=question, id_user=id_user )
        
        messages_db = ChatDataSource.get_memory_model(image, id_chat, question)
        

        [response, url_image, question_en, response_en] = ChatDataSource.get_response_model( question, image, messages_db )
        
        ChatDataSource.save_data_db_vectorial( url_image=url_image, question=question, response_split=response, id_chat=id_chat, question_en=question_en, response_en=response_en )

        
        return {
            "question": question,
            "answer": response
        }
        
        
    @staticmethod
    def get_memory_model(image: UploadFile | None, id_chat: int, question: str):
        [ vstore, embeddings, INDEX_NAME ] = VectorialDB.get_db_vectorial()
        

        messages_vectorial = vstore.similarity_search( filter={'id_chat': id_chat}, query=question, k=10 )
        
        message_image = None
        messages = []
        
        if image is None:
            messages_vectorial_images = vstore.similarity_search( filter={ "image": {"$exists": True, "$ne": ""} }, query='' )
            message_image = messages_vectorial_images[-1] if len( messages_vectorial_images ) > 0 else None
            messages.append({
                "role": message_image.metadata['role'],
                "content": [
                    {"type": "text", "text": message_image.metadata['text_en']},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": message_image.metadata['image'],
                            "detail": "low"
                        },
                    },
                ]
            })
        
        for message_data in messages_vectorial:
            messages.append({
                "role": message_data.metadata['role'],
                "content": [
                    {"type": "text", "text": message_data.metadata['text_en']}
                ]
            })
        
        return messages
    
        
    @staticmethod
    def save_data_db_vectorial( url_image: str, question: str, response_split: str, id_chat: int, question_en: str, response_en: str):

        [ vstore, embeddings, INDEX_NAME ] = VectorialDB.get_db_vectorial()
        
        vstore.from_texts(
            [question, response_split], embeddings,
            metadatas=[
                {'role': 'user', 'id_chat': id_chat, 'image': url_image, 'text_en': question_en },
                {'role': 'assistant', 'id_chat': id_chat, 'text_en': response_en}
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
    def get_response_model( question: str, image: UploadFile | None, messages: list ):
        client = ModelProcessor.get_model_processor()
        
        question_traduction = ChatDataSource.translate_text( text=question, lng="inglés" )
        
        url_image = ''
        if image:
            
            upload_result = upload(image.file, folder='chat')
            url_image = upload_result['secure_url']
            
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question_traduction
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url_image,
                                "detail": "low"
                            }
                        },
                    ]
                }
            )
        else:
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question_traduction
                        },
                    ]
                }
            )
            
        response = client.chat.completions.create(
            model='ft:gpt-4o-2024-08-06:personal::APjkVqPn',
            messages=messages
        )
        response_traduction = ChatDataSource.translate_text( text=response.choices[0].message.content, lng="español" )
        return [response_traduction, url_image, question_traduction, response.choices[0].message.content]
        
