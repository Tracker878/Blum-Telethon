from better_proxy import Proxy

from telethon import TelegramClient

from bot.config import settings
from bot.utils import logger, proxy_utils, config_utils


async def register_sessions() -> None:
    API_ID = settings.API_ID
    API_HASH = settings.API_HASH

    accounts_config_path = 'bot/config/accounts_config.json'
    proxy = None

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
        """)
        device_params.update(
            {'device_model': input('device_model: '),
             'system_version': input('system_version: '),
             'app_version': input('app_version: ')}
        )

    accounts_config = config_utils.read_or_create_config_file(accounts_config_path)
    accounts_config.update(
        {
            f'{session_name.replace(".session", "")}':
                {
                    'api_id': API_ID,
                    'api_hash': API_HASH,
                    **device_params
                }
        })

    if settings.USE_PROXY_FROM_FILE:
        proxies = proxy_utils.get_unused_proxies(accounts_config)
        if len(proxies):
            proxy = proxy_utils.to_telethon_proxy(Proxy.from_str(proxies[0]))
            accounts_config[f'{session_name.replace(".session", "")}']['proxy'] = proxies[0]
        else:
            raise Exception('No unused proxies left')
    else:
        accounts_config[f'{session_name.replace(".session", "")}']['proxy'] = None

    session = TelegramClient(f"sessions/{session_name}",
                             api_id=API_ID,
                             api_hash=API_HASH,
                             lang_code="en",
                             system_lang_code="en-US",
                             proxy=proxy if proxy else None,
                             **device_params
                             )
    await session.start()
    user_data = await session.get_me()
    if user_data:
        config_utils.write_config_file(accounts_config_path, accounts_config)
        logger.success(
            f'Session added successfully @{user_data.username} | {user_data.first_name} {user_data.last_name}')
