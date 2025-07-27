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
    max_delay = settings.failure_delay_max_minutes
    delay_seconds = random.randint(0, max_delay * 60)
    logger.info(f"Simulated failure will trigger in {delay_seconds} seconds")

    def delayed_failure():
        time.sleep(delay_seconds)

        if settings.enable_error_mode_log is True:
            _log_error()

        if settings.enable_error_mode_exception is True:
            _raise_exception()

        if settings.enable_error_mode_soft_crash is True:
            _crash_soft()

        if settings.enable_error_mode_hard_crash is True:
            _crash_hard()

        if settings.enable_error_mode_sigkill is True:
            _kill_process()

    threading.Thread(target=delayed_failure, daemon=True).start()