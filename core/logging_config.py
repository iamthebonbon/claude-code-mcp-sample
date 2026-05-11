import logging
import os


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    fmt = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter(fmt))

    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
