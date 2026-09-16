import psycopg2
from pgvector.psycopg2 import register_vector
from google import genai
from pdf_extracter import full_text
from Chunk_Maker import chunk_text
from fastapi import HTTPException 
from dotenv import load_dotenv
import os

load_dotenv()
Gemini_Api_Key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = Gemini_Api_Key )
model_id = "gemini-embedding-2"
doc_title = "Cover_Letter.pdf"

chunks = chunk_text(full_text)
for index,chunk in enumerate(chunks):
    doc_content = chunk
    formatted_doc = f"title :{doc_title} | text: {doc_content}"
    
    result = client.models.embed_content(
        model = model_id,
        contents= formatted_doc
        
    )
    if result.embeddings is None:
        raise HTTPException(
            status_code=400,
            
        )
    document_vector = result.embeddings[0].values
    
    







  