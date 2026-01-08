import os 
from dotenv import load_dotenv


class Database_Uploader:
    def __init__(self, user, password, host, port, db):
        load_dotenv()
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = os.getenv("PGDB")

    