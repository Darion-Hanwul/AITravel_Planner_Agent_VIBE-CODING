from loguru import logger

from app.config.settings import settings

logger.add(
    f"{settings.LOG_DIR}/app.log",
    rotation="10 MB",
    retention="7 days",
    level=settings.LOG_LEVEL,
)

logger.add(
    f"{settings.LOG_DIR}/error.log",
    rotation="10 MB",
    retention="30 days",
    level="ERROR",
)