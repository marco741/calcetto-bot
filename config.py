from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

_redis_endpoint = os.getenv('REDIS_ENDPOINT')
_redis_db_name = os.getenv('REDIS_DB_NAME')
_redis_username = os.getenv("REDIS_USERNAME")
_redis_password = os.getenv('REDIS_PASSWORD')
REDIS_URL = f"redis://{_redis_username}:{_redis_password}@{_redis_endpoint}/{_redis_db_name}"