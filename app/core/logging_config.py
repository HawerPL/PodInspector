import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def init_logging(log_level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = RotatingFileHandler(
        filename=LOG_DIR / "app.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5  # 10 MB
    )
    file_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
