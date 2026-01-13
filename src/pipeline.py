from collectors import *
from storage import database_loader
from utils.logger  import setup_logs, function_logs
from dotenv import load_dotenv
from utils import machine_uuid
import os
import time
from datetime import datetime

load_dotenv()
dbhost = os.getenv("DBHOST")
dbname = os.getenv("DBNAME")
dbuser = os.getenv("DBUSER")
dbpassword = os.getenv("DBPASSWORD")
sslmode = os.getenv("SSLMODE")

endtime = 15

workload_options = ['IDLE','OCCT_CPU_RAM', 'OCCT_CPU', 'OCCT_LINPACK', 'OCCT_MEMORY',
             'OCCT_3D_ADAPTIVE', 'OCCT_VRAM', 'OCCT_POWER']

chosen_workload = 'IDLE'

log = setup_logs()

uuid = machine_uuid.get_machine_uuid()

def run_pipeline():
    log.info("Pipeline Running")
    dbconnect = database_loader.Database_Uploader(dbhost, dbname, dbuser, dbpassword, sslmode, uuid)
    end = time.time() + (60 * endtime)
    date = datetime.now()

    function_logs(dbconnect.tables_setup,log)

    function_logs(dbconnect.insert_into_observed_machines,log)
    function_logs(dbconnect.insert_into_workload_types,log, workload_options)
    function_logs(dbconnect.insert_into_workload_runs,log, chosen_workload, endtime, date)

    dbconnect.conn.commit()

    insertcounter = 0
    count = 0
    while time.time() < end:
        

        cpudatadict = function_logs(cpu_collector.get_cpu_metrics,log)

        gpudatadict = function_logs(gpu_collector.get_gpu_metrics,log)

        memorydatadict = function_logs(memory_collector.get_memory_metrics,log)
        collect_date =datetime.now()

        normalizedhwdata = function_logs(dbconnect.data_normalization,log, cpudatadict, gpudatadict, memorydatadict)

        function_logs(dbconnect.insert_into_types,log, normalizedhwdata)

        if insertcounter < 1:
            function_logs(dbconnect.insert_components_into_machines, log, cpudatadict, gpudatadict)
            insertcounter += 1

        function_logs(dbconnect.insert_into_sensor_data,log, normalizedhwdata, collect_date)

        if count >= 10:
            count = 0
            dbconnect.conn.commit()
        else:
            count += 1

    dbconnect.conn.commit()
    dbconnect.conn.close()









