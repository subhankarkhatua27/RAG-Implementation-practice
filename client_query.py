from google import genai
from google.genai import types
from fastapi import HTTPException
from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")



user_query = "what are my details?"
formatted_query = f"task : search result | query : {user_query}"

client = genai.Client(api_key=GEMINI_API_KEY)
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
query_vector = user_embedding.embeddings[0].values