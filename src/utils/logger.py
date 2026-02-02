import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logs(log_file='telemetry.log'):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(format)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)

    return logger

def function_logs(func, logger, *args, workload_run_id=None, logcur=None, logconn=None, retries=3):
    for retry in range(retries):
        try:
            telemetrydata = func(*args)
            logger.info(f"{func.__name__} successfully executed")
            return telemetrydata
        except Exception as e:
            if retry < retries - 1:
                logger.warning(f"At attempt {retry} out of {retries - 1}")
            else:
                logger.error(f"{func.__name__} unsuccessfully executed workload deleted", exc_info=True)
                logcur.execute("DELETE FROM raw_sensor_data WHERE workload_run_id = %s", (workload_run_id,))
                logcur.execute("DELETE FROM raw_workload_run_data WHERE workload_run_id = %s", (workload_run_id,))
                logconn.commit()
                return None 
    

    