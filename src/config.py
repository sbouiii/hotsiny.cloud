import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    REACT_APP_KEY = os.getenv('REACT_APP_KEY')
    ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', 'http://localhost:3000')