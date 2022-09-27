import asyncio
from typings import User
from context import bot

async def notify_users(users: list[User], message: str):
    tasks = []
    for user in users:
        tasks.append(bot.send_message(user.user_id, message))
    await asyncio.gather(*tasks)