from pathlib import Path

from loguru import logger

# ==========================================================
# LOG DIRECTORY
# ==========================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(
    exist_ok=True,
)

# ==========================================================
# REMOVE DEFAULT LOGGER
# ==========================================================

logger.remove()

# ==========================================================
# CONSOLE LOGGER
# ==========================================================

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

# ==========================================================
# APPLICATION LOG
# ==========================================================

logger.add(
    LOG_DIR / "app.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="INFO",
)

# ==========================================================
# ERROR LOG
# ==========================================================

logger.add(
    LOG_DIR / "error.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="ERROR",
)

# ==========================================================
# AI LOG
# ==========================================================

logger.add(
    LOG_DIR / "ai.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG",
)

# ==========================================================
# EXPORT LOGGER
# ==========================================================

app_logger = logger

logger = app_logger