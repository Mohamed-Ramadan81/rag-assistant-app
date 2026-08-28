from fastapi import APIRouter, Request

from app.schemas.query import QueryRequest, QueryResponse
from app.services.generation import get_answer
from app.services.query_type import query_router
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health():
    return {
      "status" : "application is working"
    }


@router.post("/query",response_model= QueryResponse)
def generate_answer(data: QueryRequest, request: Request):
    route=query_router(data.question, request.app.state.ollama_client, settings.ollama_model)

    if route == "retrieve":
        answer,sources=get_answer(
            data.question,
            request.app.state.transformer,
            request.app.state.collection,
            request.app.state.ollama_client,
            settings.ollama_model,
            settings.top_k
        )
        return QueryResponse(
                answer=answer,
                sources=sources
            )

    elif route == "chat":
        answer=request.app.state.ollama_client.chat(
            model=settings.ollama_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond naturally and conversationally to the user."                    
                },
                {
                    "role": "user",
                    "content": data.question
                }
            ]
        )
        return QueryResponse(
                answer=answer["message"]["content"],
                sources=[]
            )

    else:
        return  QueryResponse(
                answer="Sorry, this question is outside the scope of this system.",
                sources=[]
            )
