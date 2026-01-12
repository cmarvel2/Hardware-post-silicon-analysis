from collectors import *
from transformers import hw_data_transformations
from utils.logger  import setup_logs, function_logs
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
dbhost = os.getenv("DBHOST")
dbname = os.getenv("DBNAME")
dbuser = os.getenv("DBUSER")
dbpassword = os.getenv("DBPASSWORD")
sslmode = os.getenv("SSLMODE")

log = setup_logs()

def run_pipeline():
    log.info("Pipeline Running")

    cpu = function_logs(cpu_collector.get_cpu_metrics,log)

    gpu = function_logs(gpu_collector.get_gpu_metrics,log)

    memory = function_logs(memory_collector.get_memory_metrics,log)

