import psycopg
import platform
from transformers import hw_data_transformations
from dotenv import load_dotenv
conn = psycopg.connect()
cur = conn.cursor()

class Database_Uploader:
    def __init__(self, user, password, host, port, db):
        load_dotenv()
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        self.hostname = platform.node()
        self.uuid = hw_data_transformations.get_machine_uuid()


    def tables_setup(cur, conn):
        cur.execute('''
            CREATE TABLE IF NOT EXISTS observed_machines (
                machine_id UUID PRIMARY KEY,
                machine_host_name, TEXT,
                cpu_model TEXT,
                gpu_model TEXT
                    )
                    ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS hardware_types
                    hardware_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hardware_name TEXT UNIQUE
                    ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS sensor_types
                    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT
                    sensor_name TEXT UNIQUE 
                    ''')
