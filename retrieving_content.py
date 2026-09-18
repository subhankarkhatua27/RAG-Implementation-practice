
from client_engine import Connecter_details
from pgvector.psycopg2 import register_vector

engine = Connecter_details.create_engine()


def vector_search_retrieve(query_vector:list[float]|None):
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
        
    retrieved_data = []
    for row in rows:
        content = row[0]
        retrieved_data.append(content)
    
    return retrieved_data