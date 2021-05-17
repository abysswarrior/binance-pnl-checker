from api_initial import privet_api_initial


def current_info_adder(exchange, assets):
    for symbol, data in assets.items():
        assets[symbol]['current_price'] = exchange.fetch_ticker(symbol + "/USDT")['last']
        assets[symbol]['current_value'] = assets[symbol]['current_price'] * assets[symbol]['amount']

    return assets


def trade_value_calculator(trade_list):
    # preprocess
    for trade in trade_list:
        if trade['side'] == 'sell':
            trade['amount'] = trade['amount'] * -1
            trade['cost'] = trade['cost'] * -1

    total_value = 0
    trade_stack = {}

    for index, data in enumerate(trade_list):

        total_value = total_value + data['amount']

        if total_value == 0:
            for stack_index, stack_data in list(trade_stack.items()):
                if int(stack_index) < index:
                    trade_stack.pop(stack_index)
        else:
            trade_stack[str(index)] = data

    average_trade_value = 0

    for trade_index, trade_data in trade_stack.items():
        average_trade_value += trade_data['cost']

    return average_trade_value


def trade_info_adder(exchange, assets):
    for symbol, data in assets.items():
        trade_info = exchange.fetch_my_trades(symbol + "/USDT")

        trade_value = trade_value_calculator(trade_info)

        assets[symbol]['trade_value'] = trade_value
        assets[symbol]['trade_price'] = trade_info[-1]['price']

    return assets


def pnl_info_adder(assets):
    for symbol, data in assets.items():
        assets[symbol]['pnl'] = data['current_value'] - data['trade_value']
        assets[symbol]['pnl_percent'] = float("{:.3f}".format((assets[symbol]['pnl'] * 100) / data['trade_value']))

    return assets


def calculate_total_info(assets, USDT_amount):
    total_pnl = 0
    total_pnl_percent = 0
    portfolio_value = 0

    for symbol, data in assets.items():
        total_pnl += data['pnl']
        total_pnl_percent += data['pnl_percent']
        portfolio_value += data['current_value']

    portfolio_value += USDT_amount

    return total_pnl , total_pnl_percent, portfolio_value


def assets_info(exchange):
    assets = {}
    account_info = exchange.fetch_balance()
    all_balances = account_info['info']['balances']

    for balance in all_balances:
        if float(balance['free']) != 0:
            assets[balance['asset']] = {'amount': account_info[balance['asset']]['free']}

    free_cash = assets['USDT']['amount']
    assets.pop('USDT', None)

    return assets, free_cash


if __name__ == '__main__':
    # initial API
    exchange = privet_api_initial()

    assets, USDT_amount = assets_info(exchange)

    # add current price and value
    assets = current_info_adder(exchange, assets)

    # add trade price and value
    assets = trade_info_adder(exchange, assets)

    # add pnl and pnl_percent
    assets = pnl_info_adder(assets)

    # calculating total info like : total pnl and total pnl percent ...
    total_pnl, total_pnl_percent, portfolio_value = calculate_total_info(assets, USDT_amount)

    print(assets)

