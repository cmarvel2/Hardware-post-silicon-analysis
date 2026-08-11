from databricks.sdk import WorkspaceClient
from src.pipeline_utils.logger import logging_setup
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging_setup()

host = os.getenv("DATABRICKS_HOST")
client_id = os.getenv("DATABRICKS_CLIENT_ID")
client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")

w = WorkspaceClient(host=host, client_id=client_id, client_secret=client_secret)

try:
    user = w.current_user.me()
    logging.info(f"User located and set")
except Exception as e:
    logging.error(f"Error in locating user: {e}")