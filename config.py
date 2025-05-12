import os
from dotenv import load_dotenv

load_dotenv()

LOCAL_PATH = os.getenv('LOCAL_PATH',)
TOKEN = os.getenv('TOKEN',)
LOG_PATH = os.getenv("LOG_PATH")
INTERVAL_SECONDS = int(os.getenv('INTERVAL_SECONDS'))

