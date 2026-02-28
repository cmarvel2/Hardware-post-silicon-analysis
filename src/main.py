from collectors import *
from storage import database_loader
from utils.logger  import setup_logs, function_logs
from dotenv import load_dotenv
from utils import machine_uuid
import os
import time
from datetime import datetime

def run_pipeline():

    load_dotenv()
    dbhost = os.getenv("DBHOST")
    dbname = os.getenv("DBNAME")
    dbuser = os.getenv("DBUSER")
    dbpassword = os.getenv("DBPASSWORD")
    sslmode = os.getenv("SSLMODE")

    endtime = 75

    test_options = ['IDLE','OCCT_CPU_RAM', 'OCCT_CPU', 'OCCT_LINPACK', 'OCCT_MEMORY',
                'OCCT_3D_ADAPTIVE', 'OCCT_VRAM', 'OCCT_POWER']

    instructionset_or_versions = ['SSE', 'AVX', 'AVX2', 'AVX512', 'Auto', '2019', '2021', 'Unavailable']

    load_type_options = ['Light', 'Heavy', 'Extreme', 'Variable', 'Steady', 'Unavailable']

    mode_type_options = ['Normal', 'Extreme', 'Unavailable']

    data_sets = ['Medium', 'Large', 'Unavailable']



    workload_test = {'Test': 'OCCT_CPU', 
                     'InstructionOrVersion' : 'SSE', 
                     'Load' : 'Steady',
                     'Mode' : 'Normal',
                     'DataSet' : 'Unavailable'
    }

    log = setup_logs()

    uuid = machine_uuid.get_machine_uuid()

    log.info("Pipeline Running")
    dbconnect = database_loader.Database_Uploader(dbhost, dbname, dbuser, dbpassword, sslmode, uuid)
    end = time.time() + (60 * endtime)
    date = datetime.now()

    function_logs(dbconnect.tables_setup,log)

    function_logs(dbconnect.insert_into_observed_machines,log)
    function_logs(dbconnect.insert_into_test_types,log, test_options)
    function_logs(dbconnect.insert_into_instorver_types,log, instructionset_or_versions)
    function_logs(dbconnect.insert_into_load_types,log, load_type_options)
    function_logs(dbconnect.insert_into_mode_types,log, mode_type_options)
    function_logs(dbconnect.insert_into_dataset_types,log, data_sets)
    workload_id = function_logs(dbconnect.insert_into_test_runs,log,workload_test['Test'] , 
                                workload_test['InstructionOrversion'], 
                                workload_test['Load'], 
                                workload_test['Mode'],
                                workload_test['DataSet'],
                                endtime, date)

    dbconnect.conn.commit()

    insertcounter = 0
    count = 0
    while time.time() < end:
        

        cpudatadict = function_logs(cpu_collector.get_cpu_metrics,
                                    log, 
                                    logcur=dbconnect.cur,
                                    logconn=dbconnect.conn,
                                    workload_run_id=workload_id)

        gpudatadict = function_logs(gpu_collector.get_gpu_metrics,
                                    log,
                                    logcur=dbconnect.cur,
                                    logconn=dbconnect.conn,
                                    workload_run_id=workload_id)

        memorydatadict = function_logs(memory_collector.get_memory_metrics,
                                       log, 
                                       logcur=dbconnect.cur,
                                       logconn=dbconnect.conn,
                                       workload_run_id=workload_id)
        
        collect_date =datetime.now()

        normalizedhwdata = function_logs(dbconnect.data_normalization,
                                        log,
                                        cpudatadict, 
                                        gpudatadict, 
                                        memorydatadict,  
                                        logcur=dbconnect.cur,
                                        logconn=dbconnect.conn,
                                        workload_run_id=workload_id)

        function_logs(dbconnect.insert_into_types,
                      log,
                      normalizedhwdata,
                      logcur=dbconnect.cur,
                      logconn=dbconnect.conn,
                      workload_run_id=workload_id)

        if insertcounter < 1:
            function_logs(dbconnect.insert_components_into_machines,
                          log,
                          cpudatadict,
                          gpudatadict,
                          logcur=dbconnect.cur,
                          logconn=dbconnect.conn,
                          workload_run_id=workload_id)
            insertcounter += 1

        function_logs(dbconnect.insert_into_sensor_data,
                      log,
                      normalizedhwdata,
                      collect_date,
                      logcur=dbconnect.cur,
                      logconn=dbconnect.conn,
                      workload_run_id=workload_id)

        if count >= 10:
            count = 0
            dbconnect.conn.commit()
        else:
            count += 1

    dbconnect.conn.commit()
    dbconnect.conn.close()

if __name__ == '__main__':
    run_pipeline()









