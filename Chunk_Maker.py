



def chunk_text(full_text:str, chunk_size=100, overlap = 50):
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunk = full_text[start:end]
        chunks.append(chunk)
        start = end - overlap
        
    return chunks


