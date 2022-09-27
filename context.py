from telethon import TelegramClient
from database import Database
import config

bot = TelegramClient('calcetto-bot', config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)
db = Database()