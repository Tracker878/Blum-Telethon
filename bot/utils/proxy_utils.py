from python_socks import ProxyType


def get_proxy_type(proxy_type: str):
    proxy_types = {
        'socks5': ProxyType.SOCKS5,
        'socks4': ProxyType.SOCKS4,
        'http': ProxyType.HTTP,
        'https': ProxyType.HTTP
    }
    return proxy_types.get(proxy_type.lower())


def to_telethon_proxy(proxy):
    return dict(
        proxy_type=get_proxy_type(proxy.protocol),
        addr=proxy.host,
        port=proxy.port,
        username=proxy.login,
        password=proxy.password
    )
