import os

from environs import Env
from loguru import logger



env = Env()
logger.info(f"Loading environment variables...")




DATA_PIPELINE_VBPL_DATABASE_URL = env.str("DATA_PIPELINE_VBPL_DATABASE_URL")
