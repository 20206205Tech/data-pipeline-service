from environs import Env
from loguru import logger

env = Env()
logger.info(f"Loading environment variables...")


DATABASE_URL = env.str("DATA_PIPELINE_VBPL_DATABASE_URL")


SUPABASE_PROJECT_ID = env.str("SUPABASE_PROJECT_ID")
SUPABASE_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co"
JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
ISSUER = f"{SUPABASE_URL}/auth/v1"
AUDIENCE = "authenticated"


print("*" * 100)
for key, value in list(globals().items()):
    if key.isupper():
        logger.info(f"{key}: ***")
print("*" * 100)
