import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

class Database_Upload:
    def __init__(self):
        load_dotenv()
        self.user = os.getenv("PGUSER")
        self.password = os.getenv("PGPASSWORD")
        self.host = os.getenv("PGHOST")
        self.port = os.getenv("PGPORT")
        self.db = os.getenv("PGDB")

