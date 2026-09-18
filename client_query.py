from google import genai
from google.genai import types
from fastapi import HTTPException
from dotenv import load_dotenv
import os
from embedding_creater import client
load_dotenv()
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")


def create_query_embedding(user_query:str):
    
    formatted_query = f"task : search result | query : {user_query}"

    #client = genai.Client(api_key=GEMINI_API_KEY)
    model_id = "gemini-embedding-2"

    user_embedding = client.models.embed_content(
        model = model_id,
        contents= formatted_query,
        config=types.EmbedContentConfig(output_dimensionality=700),
    )

    if user_embedding.embeddings is None:
        raise HTTPException(
            status_code=400,
            
        )
    return user_embedding.embeddings[0].values

