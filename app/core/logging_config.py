import datetime
import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):
    """Formatter for OpenTelemetry standard."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(
                timespec="milliseconds"
            ),
            "level": record.levelname,
            "logger": record.name,
            "record": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "otelTraceID"):
            log_entry["trace_id"] = record.otelTraceID
            log_entry["span_id"] = record.otelSpanID

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


def init_logging(log_level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = RotatingFileHandler(
        filename=LOG_DIR / "app.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setFormatter(JSONFormatter())

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
