import psycopg
import urllib.parse
from dataclasses import dataclass

@dataclass(frozen=True)
class SensorReading:
    sensorhardware: str
    sensorfield: str
    sensorname: str
    sensorvalue: float

class Database_Uploader:
    def __init__(self, host, dbname, dbuser, dbpassword, sslmode, machine_uuid):
        self.host = host
        self.dbname = dbname
        self.dbuser = urllib.parse.quote(dbuser)
        self.dbpassword = dbpassword
        self.sslmode = sslmode

        self.db_uri = f"host={self.host} dbname={self.dbname} user={self.dbuser} password={self.dbpassword} sslmode={self.sslmode}"
        self.conn = psycopg.connect(self.db_uri)
        self.cur = self.conn.cursor()

        #self.hostname = platform.node()
        self.uuid = machine_uuid
        self.conn.execute("CREATE SCHEMA IF NOT EXISTS hardware_raw")
        self.conn.execute("SET SEARCH_PATH TO hardware_raw") 

    def tables_setup(self):

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS observed_machines (
                    machine_id SERIAL PRIMARY KEY,
                    machine_uuid UUID UNIQUE NOT NULL 
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
            CREATE TABLE IF NOT EXISTS workload_types (
                    workload_id SERIAL PRIMARY KEY, 
                    workload_name TEXT UNIQUE NOT NULL
                    )  
                    ''')
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS machine_components (
                    component_entry_id SERIAL PRIMARY KEY,
                    machine_id INTEGER REFERENCES observed_machines(machine_id) NOT NULL,
                    hardware_id INTEGER REFERENCES hardware_types(hardware_id) NOT NULL,
                    UNIQUE(machine_id, hardware_id)
                         )''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS raw_workload_run_data (
                    workload_run_id SERIAL PRIMARY KEY,
                    machine_id INTEGER REFERENCES observed_machines(machine_id) NOT NULL,
                    workload_id INTEGER REFERENCES workload_types(workload_id) NOT NULL,
                    runtime_mins INTEGER NOT NULL,
                    run_date TIMESTAMP NOT NULL,
                    UNIQUE (machine_id, workload_id, runtime_mins, run_date)
                    )''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS raw_sensor_data (
                    sensor_entry_id SERIAL PRIMARY KEY,
                    machine_id INTEGER REFERENCES observed_machines(machine_id) NOT NULL,
                    workload_run_id INTEGER REFERENCES raw_workload_run_data(workload_run_id) NOT NULL,
                    hardware_id INTEGER REFERENCES hardware_types(hardware_id) NOT NULL,
                    hardware_field_id INTEGER REFERENCES hardware_fields(field_id) NOT NULL,
                    sensor_id INTEGER REFERENCES sensor_types(sensor_id) NOT NULL,
                    sensor_value NUMERIC,
                    collection_ts TIMESTAMP NOT NULL,
                    UNIQUE(workload_run_id, hardware_id, hardware_field_id, sensor_id, collection_ts)
                    )''')
        
        self.conn.commit()

    def data_normalization(self, cpudata, gpudata, memorydata):
        hwdatalist = []

        for cpuhwname, cpufield in cpudata.items():
            for cpuhwfield, cpuhwsubpartdict in cpufield.items():
                for cpuhwsubpart, cpuvalue in cpuhwsubpartdict.items():

                    hwdatalist.append(SensorReading(sensorhardware=cpuhwname, sensorfield=cpuhwfield, sensorname=cpuhwsubpart, sensorvalue=cpuvalue))

        for gpu in gpudata: 
                               
            for gpuhwname, gpufield in gpu.items():
                for gpuhwfield, gpuhwsubpartdict in gpufield.items():
                    for gpuhwsubpart, gpuvalue in gpuhwsubpartdict.items():

                        hwdatalist.append(SensorReading(sensorhardware=gpuhwname, sensorfield=gpuhwfield, sensorname=gpuhwsubpart, sensorvalue=gpuvalue))

        for memhwfield, memfield in memorydata.items():
            for memhwsubpart, memvalue in memfield.items():

                hwdatalist.append(SensorReading(sensorhardware='Random Access Memory', sensorfield=memhwfield, sensorname=memhwsubpart, sensorvalue=memvalue))

        return hwdatalist

    def insert_into_observed_machines(self):

        self.cur.execute(
             '''INSERT INTO observed_machines 
                (machine_uuid) 
                VALUES (%s)
                ON CONFLICT DO NOTHING''',
                (self.uuid,)
                )
        
    def insert_components_into_machines(self, cpudatadict, gpudatadict):
        processorlist = []

        for cpuname in cpudatadict.keys():
            processorlist.append(cpuname)

        for gpu in gpudatadict:
            for gpuname in gpu.keys():
                processorlist.append(gpuname)
            
        self.cur.execute('SELECT machine_id FROM observed_machines WHERE machine_uuid = %s', (self.uuid,))
        machine_id = self.cur.fetchone()[0]

        for processor_fact in processorlist:
            self.cur.execute('SELECT hardware_id FROM hardware_types WHERE hardware_name = %s', (processor_fact,))
            hardware_id = self.cur.fetchone()[0]

            self.cur.execute(
                '''INSERT INTO machine_components (machine_id, hardware_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING''',
                    (machine_id,
                     hardware_id,)
                    )
        
    def insert_into_types(self, normalized_hw_data):
        for row in normalized_hw_data:
            self.cur.execute(
                '''INSERT INTO hardware_types (hardware_name)
                    VALUES (%s)
                    ON CONFLICT DO NOTHING''',
                    (row.sensorhardware,)
                    )
                
            self.cur.execute(
                '''INSERT INTO hardware_fields (hardware_field)
                    VALUES (%s)
                    ON CONFLICT DO NOTHING''',
                    (row.sensorfield,)
                    )
                
            self.cur.execute(
                '''INSERT INTO sensor_types (sensor_name)
                    VALUES(%s)
                    ON CONFLICT DO NOTHING''',
                    (row.sensorname,)
                    )
                        
    def insert_into_workload_types(self, testlist):
        for test_type in testlist:
            self.cur.execute(
                '''INSERT INTO workload_types (workload_name)
                VALUES(%s)
                ON CONFLICT DO NOTHING''',
                (test_type,)
                )

    def insert_into_workload_runs(self, workloadstring, runtime_mins, run_date):
        self.cur.execute('SELECT machine_id FROM observed_machines WHERE machine_uuid = %s', (self.uuid,))
        machine_id = self.cur.fetchone()[0]

        self.cur.execute('SELECT workload_id FROM workload_types WHERE workload_name = %s', (workloadstring,))
        workload_id = self.cur.fetchone()[0]

        self.cur.execute(
            '''INSERT INTO raw_workload_run_data (machine_id, workload_id, runtime_mins, run_date)
                VALUES(%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                RETURNING workload_run_id''',
                (machine_id,
                 workload_id,
                 runtime_mins,
                 run_date,)
                )
        self.workload_run_id = self.cur.fetchone()[0]

        return self.workload_run_id
        
    def insert_into_sensor_data(self, normalized_hw_data, timestamp):
        self.cur.execute('SELECT machine_id FROM observed_machines WHERE machine_uuid = %s', (self.uuid,))
        machine_id = self.cur.fetchone()[0]
        
        for row in normalized_hw_data:
            self.cur.execute('SELECT hardware_id FROM hardware_types WHERE hardware_name = %s', (row.sensorhardware,))
            hardware_id = self.cur.fetchone()[0]

            self.cur.execute('SELECT field_id FROM hardware_fields WHERE hardware_field = %s', (row.sensorfield,))
            field_id = self.cur.fetchone()[0]

            self.cur.execute('SELECT sensor_id FROM sensor_types WHERE sensor_name = %s', (row.sensorname,))
            sensortype_id = self.cur.fetchone()[0]

        
            self.cur.execute(
                '''INSERT INTO raw_sensor_data (machine_id, workload_run_id, hardware_id, hardware_field_id, sensor_id, sensor_value, collection_ts)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING''',
                    (machine_id,
                    self.workload_run_id,
                    hardware_id,
                    field_id,
                    sensortype_id,
                    row.sensorvalue,
                    timestamp,)
        )
            