import psycopg
import platform
import urllib.parse
import psutil
from transformers import hw_data_transformations



class Database_Uploader:
    def __init__(self, host, dbname, dbuser, dbpassword, sslmode):
        self.host = host
        self.dbname = dbname
        self.dbuser = urllib.parse.quote(dbuser)
        self.dbpassword = dbpassword
        self.sslmode = sslmode

        self.db_uri = f"host={self.host} dbname={self.dbname} user={self.dbuser} password={self.dbpassword} sslmode={self.sslmode}"
        self.conn = psycopg.connect()
        self.cur = self.conn.cursor()

        self.hostname = platform.node()
        self.uuid = hw_data_transformations.get_machine_uuid()


    def tables_setup(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS observed_machines (
                    machine_uuid UUID PRIMARY KEY,
                    machine_host_name TEXT,
                    cpu_model TEXT,
                    gpu_model TEXT  
                    )''')
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS hardware_types (
                    hardware_id SERIAL PRIMARY KEY,
                    hardware_name TEXT UNIQUE NOT NULL
                    )''')
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS hardware_fields (
                    field_id SERIAL PRIMARY KEY,
                    hardware_field TEXT UNIQUE NOT NULL
                    )''')
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS sensor_types (
                    sensor_id SERIAL PRIMARY KEY,
                    sensor_name TEXT UNIQUE NOT NULL
                    )''')
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS workload_programs (
                    workload_id SERIAL PRIMARY KEY, 
                    workload_name TEXT UNIQUE NOT NULL
                    )  
                    ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS raw_workload_run_data (
                    workload_run_id SERIAL PRIMARY KEY,
                    machine_uuid UUID REFERENCES observed_machines(machine_uuid) NOT NULL,
                    workload_id INTEGER REFERENCES workload_programs(workload_id) NOT NULL,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP

                    )''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS raw_sensor_data (
                    sensor_entry_id SERIAL PRIMARY KEY,
                    machine_uuid UUID REFERENCES observed_machines(machine_uuid) NOT NULL,
                    workload_run_id INTEGER REFERENCES raw_workload_run_data(workload_run_id) NOT NULL,
                    hardware_id INTEGER REFERENCES hardware_types(hardware_id) NOT NULL,
                    hardware_field_id INTEGER REFERENCES hardware_fields(field_id) NOT NULL,
                    sensor_id INTEGER REFERENCES sensor_types(sensor_id) NOT NULL,
                    sensor_value NUMERIC NOT NULL,
                    collection_ts TIMESTAMP NOT NULL,
                    UNIQUE(workload_run_id, hardware_id, hardware_field_id, sensor_id, collection_ts)
                    )''')
        
        self.conn.commit()

    def insert_into_observed_machines(self, cpudata, gpudata):
        cpulist = []
        gpulist = []

        for cpuname in cpudata.keys():
            cpulist.append(cpuname)

        for gpu in gpudata:
            for gpuname in gpu.items():
                gpulist.append(gpuname)

        cpumodels = ','.join(cpulist)
        gpumodels = ','.join(gpulist)

        self.cur.execute(
             '''INSERT INTO observed_machines 
                (machine_uuid, machine_host_name, cpu_model, gpu_model) 
                VALUES (?,?,?,?,)
                ON CONFLICT (machine_uuid) DO NOTHING''',
                (self.uuid,
                self.hostname,
                cpumodels, 
                gpumodels))
        
        self.conn.commit()
        
    def insert_into_types_cpudata(self, cpudata):
            for hwname, field in cpudata.items():
                for hwfield, hwsubpartdict in field.items():
                    for hwsubpart, _ in hwsubpartdict.items():
                        self.cur.execute(
                            '''INSERT INTO hardware_types (hardware_name)
                                VALUES (?,)
                                ON CONFLICT (hardware_name) DO NOTHING''',
                                (hwname)
                                )
                        
                        self.cur.execute(
                            '''INSERT INTO hardware_fields (hardware_field)
                                VALUES (?,)
                                ON CONFLICT (hardware_field) DO NOTHING'''
                                (hwfield)
                                )
                        
                        self.cur.execute(
                            '''INSERT INTO sensor_types (sensor_name)
                                VALUES(?)
                                ON CONFLICT (sensor_name) DO NOTHING'''
                                (hwsubpart)
                                )
                        
            self.conn.commit()

    def insert_into_types_gpudata(self, gpudata):
        for gpu in gpudata:                    
            for hwname, field in gpu.items():
                for hwfield, hwsubpartdict in field.items():
                    for hwsubpart, _ in hwsubpartdict.items():
                        self.cur.execute(
                            '''INSERT INTO hardware_types (hardware_name)
                                VALUES (?,)
                                ON CONFLICT (hardware_name) DO NOTHING''',
                                (hwname)
                                )
                        
                        self.cur.execute(
                            '''INSERT INTO hardware_fields (hardware_field)
                                VALUES (?,)
                                ON CONFLICT (hardware_field) DO NOTHING'''
                                (hwfield)
                                )
                        
                        self.cur.execute(
                            '''INSERT INTO sensor_types (sensor_name)
                                VALUES(?)
                                ON CONFLICT (sensor_name) DO NOTHING'''
                                (hwsubpart)
                                )
        
        self.conn.commit()

    def insert_into_types_memory(self,memorydata):
        for hwfieldname, field in memorydata.items():
            for sensorname, _ in field.items():
                self.cur.execute(
                    '''INSERT INTO hardware_types (hardware_name)
                        VALUES (?,)
                        ON CONFLICT (hardware_name) DO NOTHING''',
                        ("Random Access Memory")
                        )
                        
                self.cur.execute(
                    '''INSERT INTO hardware_fields (hardware_field)
                        VALUES (?,)
                        ON CONFLICT (hardware_field) DO NOTHING'''
                        (hwfieldname)
                        )
                        
                self.cur.execute(
                    '''INSERT INTO sensor_types (sensor_name)
                        VALUES(?)
                        ON CONFLICT (sensor_name) DO NOTHING'''
                        (sensorname)
                        )

    def insert_into_workload(self, workloadstring):

        self.cur.execute('''INSERT INTO )
