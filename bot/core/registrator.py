from better_proxy import Proxy

from telethon import TelegramClient

from bot.config import settings
from bot.utils import logger, proxy_utils

from os.path import join


async def register_sessions() -> None:
    API_ID = settings.API_ID
    API_HASH = settings.API_HASH

    if not API_ID or not API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    session_name = input('\nEnter the session name (press Enter to exit): ').strip() + ".session"

    if not session_name:
        return None

    device_params = {}
    if settings.DEVICE_PARAMS:
        print("""Sample Device values:
        ### Attributes:
            device_model (`str`)     : `"Samsung SM-G998B"`
            system_version (`str`)   : `"SDK 31"`
            app_version (`str`)      : `"8.4.1 (2522)"`
            system_lang_code (`str`) : `"en-US"`
        """)
        device_params.update(
            {'device_model': input('device_model: '),
             'system_version': input('system_version: '),
             'app_version': input('app_version: ')}
        )
    session = TelegramClient(f"sessions/{session_name}",
                             api_id=API_ID,
                             api_hash=API_HASH,
                             system_lang_code="en-US",
                             **device_params
                             )
    await session.start()
    user_data = await session.get_me()

    logger.success(f'Session added successfully @{user_data.username} | {user_data.first_name} {user_data.last_name}')
