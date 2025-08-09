import logging
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel
from typing import Union,Optional,List
from Config.config import get_settings
from enum import Enum

class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"
    TASK_DESCRIPTION = "Given a user query, retrieve relevant passages that answer the query"  

class e5Model:
    def __init__(self,model_name):
        self.settings = get_settings()
        
        self.embedding_model = HuggingFaceEmbeddings(model_name=model_name,
                                                     cache_folder="./embedding" )
        self.logger = logging.getLogger(__name__)
        
    async def embed_text(self, text: Union[str,List[str]], document_type: str = None):
        try:
            
            if document_type == DocumentTypeEnum.QUERY.value:
                text = await self.add_instruct(DocumentTypeEnum.TASK_DESCRIPTION.value, text)
                embeddings = await self.embedding_model.aembed_query(text=text)
            
            if isinstance(text, str):
                embeddings = await self.embedding_model.aembed_query(text=text)   
            else:
                embeddings = await self.embedding_model.aembed_documents(texts=text)
   
            if  len(embeddings) == 0 :
                self.logger.error("Error while Embedding text with E5")
                return None
        
        except Exception as e:
            self.logger.error(f"Error while Embedding text with E5: {e}")
            return None
        
        return embeddings
    
    async def add_instruct(self, task_description, user_query):
        return f'Instruct: {task_description}\nQuery: {user_query}'