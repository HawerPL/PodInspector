import logging
import os
import sys
import signal
import random
import time
import threading
import platform

from app.core.settings import settings

logger = logging.getLogger(__name__)


def _crash_hard():
    logger.warn("Triggering hard crash via os._exit(1)")
    os._exit(1)


def _crash_soft():
    logger.warning("Triggering soft crash via sys.exit(1)")
    sys.exit(1)


def _raise_exception():
    logger.warning("Triggering uncaught exception")
    raise RuntimeError("Simulated uncaught exception")


def _kill_process():
    logger.warning("Sending SIGKILL to self")
    if platform.system() == "Windows":
        # os._exit działa również na Windowsie
        os._exit(1)
    else:
        os.kill(os.getpid(), signal.SIGKILL)


def _log_error():
    logger.error("Simulated error log entry")


def simulate_failure():
    logging.info("Error mode is enabled")
    max_delay = settings.FAILURE_DELAY_MAX_MINUTES
    delay_seconds = random.randint(0, max_delay * 60)
    logger.info(f"Simulated failure will trigger in {delay_seconds} seconds")

    def delayed_failure():
        time.sleep(delay_seconds)

        if settings.ENABLE_ERROR_MODE_LOG is True:
            _log_error()

        if settings.ENABLE_ERROR_MODE_EXCEPTION is True:
            _raise_exception()

        if settings.ENABLE_ERROR_MODE_SOFT_CRASH is True:
            _crash_soft()

        if settings.ENABLE_ERROR_MODE_HARD_CRASH is True:
            _crash_hard()

        if settings.ENABLE_ERROR_MODE_SIGKILL is True:
            _kill_process()

    threading.Thread(target=delayed_failure, daemon=True).start()
