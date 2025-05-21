import sys

from config import LOG_PATH
from loguru import logger

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "syn_service: {file}  {time:YYYY-MM-DD HH:MM:SS} {level} {message}",
        },
        {"sink": f"{LOG_PATH}", "serialize": True},
    ],
    "extra": {"user": "someone"},
}

logger.configure(**config)
