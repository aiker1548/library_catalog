import os
from loguru import logger

log_dir = os.getenv("API_CLIENT_LOG_DIR", "logs")
os.makedirs(log_dir, exist_ok=True)

logger.remove() 
logger.add(
    os.path.join(log_dir, "api_client.log"),
    rotation="10 MB",
    retention="14 days",
    compression="zip",
    level="INFO",
)
