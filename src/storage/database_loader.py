import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

class Database_Uploader:
    def __init__(self, user, password, host, port, db):
        load_dotenv()
        self.user = user
        self.password = password
        self.host = host
        self.port = os.getenv("PGPORT")
        self.db = os.getenv("PGDB")

    