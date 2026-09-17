import psycopg2
from pgvector.psycopg2 import register_vector
from pgvector import vector
from google import genai
from google.genai import types
from pdf_extracter import full_text
from Chunk_Maker import chunk_text
from client_query import query_vector
from fastapi import HTTPException
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
Gemini_Api_Key = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise HTTPException(
        status_code=404,
    )

engine = create_engine(DATABASE_URL)


client = genai.Client(api_key = Gemini_Api_Key )
model_id = "gemini-embedding-2"
doc_title = "Cover_Letter.pdf"

chunks = chunk_text(full_text)
for index,chunk in enumerate(chunks):
    doc_content = chunk
    formatted_doc = f"title :{doc_title} | text: {doc_content}"
    
    result = client.models.embed_content(
        model = model_id,
        contents= formatted_doc,
        config=types.EmbedContentConfig(output_dimensionality=700),   #applying the limit of 700 values of embedding in vector
        
    )
    if result.embeddings is None:
        raise HTTPException(
            status_code=400,
            
        )
    document_vector = result.embeddings[0].values
    
    with engine.raw_connection() as conn:
        register_vector(conn.connection)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO pgvector (source_file, chunk_index, content, embedding) VALUES (%s, %s, %s, %s)",
                (doc_title, index, formatted_doc, document_vector),
            )
        finally:
            cursor.close()
        conn.commit()

rows = ()   
with engine.raw_connection() as conn:
    register_vector(conn.connection)
    cursor= conn.cursor()
    try:
        cursor.execute(
            "SELECT content, 1-(embedding <=> %s::vector) AS similarity  FROM pgvector ORDER BY embedding <=> %s::vector  LIMIT 5;",
            (query_vector,query_vector)
        )
        rows = cursor.fetchall()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
    
    conn.commit()
        
print(rows)           
            
                       
                                  
                                  
    
    
    







  