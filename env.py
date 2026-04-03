import os

from environs import Env
from loguru import logger

# _file_format = "{time:YYYY-MM-DD}.log"
# ger.add(
   # f"logging/{log_file_format}", rotation="00:00", retention="7 days", enqueue=True



env = Env()
logger.info(f"Loading environment variables...")


PATH_FILE_ENV = os.path.abspath(__file__)
PATH_FOLDER_PROJECT = os.path.dirname(PATH_FILE_ENV)
PATH_FOLDER_DATA = os.path.join(PATH_FOLDER_PROJECT, "data")
PATH_FOLDER_DOCS = os.path.join(PATH_FOLDER_PROJECT, "docs")


if not os.path.exists(PATH_FOLDER_DATA):
    os.makedirs(PATH_FOLDER_DATA)

if not os.path.exists(PATH_FOLDER_DOCS):
    os.makedirs(PATH_FOLDER_DOCS)


DATA_PIPELINE_VBPL_DATABASE_URL = env.str("DATA_PIPELINE_VBPL_DATABASE_URL")
