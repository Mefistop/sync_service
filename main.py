import sys
from src.core.sync_engine import SyncEngine
from config import LOCAL_PATH, TOKEN, INTERVAL_SECONDS, LOG_PATH
from src.utils.logger import logger

def validate_config():
    """Validates the configuration parameters loaded from the `config` module. """
    if not LOCAL_PATH or not TOKEN or not LOG_PATH or INTERVAL_SECONDS <= 0:
        logger.error('Ошибка: проверьте настройки в config.py.')
        sys.exit(1)

def main():
    """Main entry point for the application."""
    validate_config()
    app=SyncEngine(local_path= LOCAL_PATH, token=TOKEN)
    app.run_periodical(interval_seconds=INTERVAL_SECONDS)

if __name__ == '__main__':
    main()