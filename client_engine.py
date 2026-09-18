from sqlalchemy import create_engine
from google import genai
from dotenv import load_dotenv
from fastapi import HTTPException
import os
load_dotenv()

class Connecter_details:
    @staticmethod
    def create_engine():
        DATABASE_URL = os.getenv("DATABASE_URL")
        if DATABASE_URL is None:
            raise HTTPException(
            status_code=404,
        )
        engine = create_engine(DATABASE_URL)
        return engine

    @staticmethod
    def create_client():
        Gemini_Api_Key = os.getenv("GEMINI_API_KEY")
        if Gemini_Api_Key is None:
            raise HTTPException(
            status_code=404,
        )
        client = genai.Client(api_key = Gemini_Api_Key ) 
        return client   