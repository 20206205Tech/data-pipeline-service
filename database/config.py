from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import env
from utils.log_function import log_function

DATABASE_URL = env.DATA_PIPELINE_VBPL_DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@log_function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
