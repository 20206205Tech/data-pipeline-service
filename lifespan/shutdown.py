from loguru import logger


async def shutdown():
    logger.info("Shutting down application...")
