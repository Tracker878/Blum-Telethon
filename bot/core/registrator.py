import asyncio

from opentele.tl import TelegramClient
from opentele.api import API

from bot.config import settings
from bot.utils import logger

from os.path import join


async def register_sessions() -> None:
    API_ID = settings.API_ID
    API_HASH = settings.API_HASH

    if not API_ID or not API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    session_name = input('\nEnter the session name (press Enter to exit): ').strip() + ".session"

    if not session_name:
        return None

    api = API.TelegramIOS.Generate(unique_id=session_name)
    session_abs_path = join(settings.PROJECT_ROOT, "sessions", session_name)

    session = TelegramClient(session_abs_path, api_id=API_ID, api_hash=API_HASH) if API_ID and API_HASH \
        else TelegramClient(session_abs_path, api=api)
    session.start()
    async with session:
        user_data = await session.get_me()

    logger.success(f'Session added successfully @{user_data.username} | {user_data.first_name} {user_data.last_name}')

asyncio.run(register_sessions())
