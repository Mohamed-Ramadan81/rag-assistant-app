from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import chromadb
from app.core.config import settings
from app.api.routes.query import router
import ollama

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.transformer=SentenceTransformer(settings.model_transformer, device="cuda")

    client=chromadb.PersistentClient(settings.vector_store_path)

    app.state.collection=client.get_collection("Harry_Potter")

    app.state.ollama_client = ollama.Client(host=settings.ollama_host)
                            

    yield

app=FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin])

app.include_router(router)









