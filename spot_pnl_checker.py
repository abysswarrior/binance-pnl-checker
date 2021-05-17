from api_initial import privet_api_initial


def assets_info(exchange):
    assets = {}
    account_info = exchange.fetch_balance()
    all_balances = account_info['info']['balances']

    for balance in all_balances:
        if float(balance['free']) != 0:
            assets[balance['asset']] = account_info[balance['asset']]

    return assets


if __name__ == '__main__':
    # initial API
    exchange = privet_api_initial()

    assets = assets_info(exchange)

    for symbol in assets.keys():
        try:
            print(exchange.fetch_orders(symbol=symbol + "/USDT"))
        except:
            continue
