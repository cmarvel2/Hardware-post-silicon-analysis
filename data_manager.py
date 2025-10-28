import pandas as pd
import sqlite3 as db
from sqlalchemy import create_engine
from System_data import Sysdata
from datetime import datetime

class Data_formatter:
    
    def __init__(self, hardware_data, process_data):
        self.hardware_data =  pd.DataFrame(hardware_data)
        self.process_data = pd.DataFrame(process_data)
    
    def sql_connector(self):
        engine = create_engine("sqlite+pysqlite:///Hwdata.db", echo=True, future=True)

        self.hardware_data.to_sql(name='HardwareDatabase', con=engine)
        self.process_data.to_sql(name="ProcessesDatabse", con=engine)
   

system = Sysdata()
systemdata= system.get_telemetry()
processdata= system.get_top_processes()
formatteddata = Data_formatter(systemdata,processdata)
#print(formatteddata.System_telemetry_dataframe())
#print(formatteddata.processor_data_dataframe())


#print(datetime.today())