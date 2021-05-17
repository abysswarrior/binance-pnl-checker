import ccxt
from decouple import config


def privet_api_initial():
    """
    connect to binance privet api
    """
    exchange = ccxt.binance({'apiKey': config('API_KEY'),
                             'secret': config('SECRET_KEY'),
                             'options': {
                                 'defaultType': 'spot'  # change to desire market
                             },
                             'enableRateLimit': True})

    if config('RESTRICTED', cast=bool):
        exchange.proxies = {
            'http': f'socks5h://{config("PROXY_HOST")}:{config("PROXY_POST")}',
            'https': f'socks5h://{config("PROXY_HOST")}:{config("PROXY_POST")}',
        }

    return exchange
