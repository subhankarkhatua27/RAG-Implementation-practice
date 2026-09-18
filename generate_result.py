from pdf_extracter import pdf_extracter
from Chunk_Maker import chunk_text
from embedding_creater import embed_document
from client_query import create_query_embedding
from retrieving_content import vector_search_retrieve
from fastapi import HTTPException
from client_engine import Connecter_details


client = Connecter_details.create_client()
def generate_result(query:str,document:str):
    
    full_text = pdf_extracter(document)
    chunks = chunk_text(full_text)
    embed_document(chunks, document)
    query_vector = create_query_embedding(query)
    if query_vector is None:
        raise HTTPException(
            status_code = 400,
        )
    
    
    retrieved_data = vector_search_retrieve(query_vector)
    
    context = "\n\n".join(retrieved_data)
    prompt = f"""Answer the question using ONLY the provided context.
    If the answer is not in the context, say exactly:
    'I cannot find this information in the provided documents.'
    Do not use any knowledge outside the provided context.

    Context:
    {context}

    Question: {query}

    Answer:"""           
            
    #response = client.models.generate_content(
        #model= "gemini-2.5-flash",
        #contents = prompt
    #)
    #print(response.text)                       


    chat = client.chats.create(model = "gemini-2.5-flash")
    return  chat.send_message(prompt)

print(generate_result("what are my details?","Cover_Letter.pdf"))

if __name__ == "__main__":
    print(generate_result("what are my details?", "Cover_Letter.pdf"))