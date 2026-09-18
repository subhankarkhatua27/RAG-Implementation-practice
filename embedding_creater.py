
from pgvector.psycopg2 import register_vector
from google.genai import types
from fastapi import HTTPException
from client_engine import Connecter_details
from pathlib import Path

model_id = "gemini-embedding-2"
engine = Connecter_details.create_engine()
client = Connecter_details.create_client()

def embed_document(chunks: list[str], source_file: str):
    doc_title = Path(source_file).name
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
   





    

                                  
    
    
    







  