from fastapi import APIRouter , Depends,UploadFile , status, Request
from fastapi.responses import JSONResponse
import os
import aiofiles
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import shutil

data_router = APIRouter(prefix="/api/data", tags=["Data"])

@data_router.post("/upload")
async def process_endpoint(request : Request, file : UploadFile):
    
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "response": "File Type Not Supported"
            }
        )
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temporary files")
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    
    async with aiofiles.open(file_path,'wb') as f :
            while chunk:= await file.read(512000):
                await f.write(chunk)
    
    loader = PyMuPDFLoader(file_path = file_path)
    
    file_content = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 250,
            chunk_overlap = 50,
            length_function = len,
        )
    
    chunks = await text_splitter.atransform_documents(
            documents=file_content,
        )
    
    for i in range(0,len(chunks),50):
        # Get the current batch
        batch = chunks[i:i + 50]
        # Extract documents, metadata, and IDs for the batch
        documents = [chunk.page_content for chunk in batch]
        metadata = [chunk.metadata for chunk in batch]
        vectors = []
        inserted = request.app.db_client.insert_documents(collection_name = "ay haga",documents=documents,embedding_vectors=vectors,metadata=metadata,batch_size=50)
    
    
    if not inserted:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "response": "Failed To save Files to the database",   
            }
        )
    
    shutil.rmtree(file_path)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "response":"File Added Successfully",
            "Inserted Chunks": len(chunks),
            'File name':file.filename,
        }
    )
