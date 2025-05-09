from loguru import logger
from config import LOG_PATH, PATH
import sys

config = {
    "handlers": [
        {"sink": sys.stdout, "format": "syn_service:{file} {time:YYYY-MM-DD HH:MM:SS} {level} {message}"},
        {"sink": f"..{LOG_PATH}", 'serialize': True},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)

logger.info(f"Программа синхронизации файлов начинат работать с директорией '{PATH}'")
