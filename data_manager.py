import pandas as pd
import sqlite3 as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database



class Data_formatter:
    
    def __init__(self, hardware_data, process_data, timestamp):

        self.hardware_data =  pd.DataFrame(hardware_data)
        self.process_data = pd.DataFrame(process_data)

        self.hardware_data["Timestamp"] = timestamp
        self.process_data["Timestamp"] = timestamp
    
    def sql_connector(self, user, password, host, port, db):
        url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        if not database_exists(url):
            create_database(url)

        engine=create_engine(url, pool_size=50, echo=False)
                               

        self.hardware_data.to_sql(name='HardwareDatabase', con=engine, if_exists='append', index=False)
        self.process_data.to_sql(name="ProcessesDatabase", con=engine, if_exists='append', index=False)
   

