from system_data import Sysdata
from data_manager import Data_formatter
from dotenv import load_dotenv
import os
import datetime


def main():
    system = Sysdata()
    processesinfo = system.get_top_processes()
    hardwareinfo = system.get_telemetry()

    currtime = datetime.datetime.now()
    load_dotenv()
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    host = os.getenv("PGHOST")
    port = os.getenv("PGPORT")
    db = os.getenv("PGDB")

    formatteddata = Data_formatter(hardwareinfo,processesinfo,currtime)
    formatteddata.sql_connector(user, password, host, port, db)

if __name__ == "__main__":
    main()