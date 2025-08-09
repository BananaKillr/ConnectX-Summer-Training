from fastapi.responses import JSONResponse
from fastapi import APIRouter , status,Depends,Header,HTTPException,Request
from Config.config import get_settings
from langchain_core.messages import AIMessage,HumanMessage
from pydantic import BaseModel
from Agents.LangGraphAgent import LangGraphAgent 

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

 # your class

# chat_router = APIRouter(tags=['LangGraph'], prefix='/api/langgraph')

# Initialize the agent once (so it persists across requests)
langgraph_agent = LangGraphAgent()

@chat_router.post("/chat_langgraph")
async def chat_with_langgraph(request: Request, user_request: QuestionRequest):
    config = {"configurable": {"thread_id": "streamlit_session"}}
    initial_state = {
        "user_id": 1,
        "messages": [HumanMessage(content=user_request.question)],
    }
    result = langgraph_agent.graph.invoke(initial_state, config)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "response": result['messages'][-1].content
        }
    )
