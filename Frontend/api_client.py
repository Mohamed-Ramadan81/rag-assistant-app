import os
import requests as rq
from dotenv import load_dotenv


load_dotenv()

backend_url=os.getenv("API_BASE_URL")

def query(question):
    data={"question": question}

    response=rq.post(f"{backend_url}/query" , json=data, timeout=150)
    response.raise_for_status()

    return response.json()

