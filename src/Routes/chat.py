from fastapi.responses import JSONResponse
from fastapi import APIRouter , status,Depends,Header,HTTPException,Request
from Config.config import get_settings
from pydantic import BaseModel

chat_router = APIRouter(tags=['Chat'], prefix='/api/chat')

class QuestionRequest(BaseModel):
    question: str

@chat_router.post("/chat")
async def chat(request: Request,
               user_request: QuestionRequest):

    # 1. Embed User Query:
    user_query_embedding = await request.app.embedding_client.embed_text(text=user_request.question,document_type="query")

    # 2. Get Similiar results from vector database:
    topk_results = request.app.db_client.search_by_vector(collection_name='Documents',query_vector=user_query_embedding, top_k=12)
    
    # 3. Join context from results
    context = "\n".join(result.payload.get("text", "") for result in topk_results)
    print(f"Context:{context}\n")


    # 4. Send the context and question to our LLM and get back response
    response =  request.app.llm.run(user_question=user_request.question,
                                         retrieved_context=context)
    print(response)
    
    if response is not None:
         return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "response":response.content ,
            }
        )
    else:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "response": None ,
            }
        )

    
