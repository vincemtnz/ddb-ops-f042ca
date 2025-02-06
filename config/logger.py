import logging
import os

def setup_logger():
    logging.basicConfig()
    log = logging.getLogger("pynamodb")
    log.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    log.propagate = True
