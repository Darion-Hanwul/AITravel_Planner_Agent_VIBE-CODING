from pathlib import Path

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(
    exist_ok=True,
)

logger.remove()

logger.add(
    sink=lambda msg: print(msg, end=""),
    level="INFO",
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

logger.add(
    LOG_DIR / "app.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="INFO",
)

logger.add(
    LOG_DIR / "error.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="ERROR",
)

logger.add(
    LOG_DIR / "ai.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG",
)

app_logger = logger

logger = app_logger