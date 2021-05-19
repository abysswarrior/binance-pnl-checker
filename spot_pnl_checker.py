from api_initial import privet_api_initial
from colorama import Fore, Style, init
from prettytable import PrettyTable
import pyfiglet

init(autoreset=True)


def current_info_adder(exchange, assets):
    """
    check realtime price and calculate assets current value
    and added to assets dictionary

    Args:
        exchange: ccxt object
        assets: list of coins in the asset

    Returns:
        assets with new data
    """
    for symbol, data in assets.items():
        # get symbol data from binance
        assets[symbol]['current_price'] = exchange.fetch_ticker(symbol + "/USDT")['last']
        assets[symbol]['current_value'] = assets[symbol]['current_price'] * assets[symbol]['amount']

    return assets


def trade_value_calculator(trade_list):
    """
    calculate trade value base on trade history
    if you bay/sell one coin multiple times it's complicated
    to find out trade value. this function check all trade history
    and filter trades that completely filled to avoid mistaken

    Args:
        trade_list: trade history

    Returns:
        average trade value
    """
    # preprocess
    for trade in trade_list:
        if trade['side'] == 'sell':
            trade['amount'] = trade['amount'] * -1
            trade['cost'] = trade['cost'] * -1

    total_value = 0
    # stack
    trade_stack = {}

    for index, data in enumerate(trade_list):

        total_value = total_value + data['amount']

        # trade history is even
        if total_value == 0:

            # so remove previous trades from stack
            for stack_index, stack_data in list(trade_stack.items()):
                if int(stack_index) < index:
                    trade_stack.pop(stack_index)
        # add to stack
        else:
            trade_stack[str(index)] = data

    average_trade_value = 0

    # sum all cost of remaining trades in stack
    for trade_index, trade_data in trade_stack.items():
        average_trade_value += trade_data['cost']

    return average_trade_value


def trade_info_adder(exchange, assets):
    """
    get trade history and add trade value + trade price
    to assets

    Args:
        exchange: ccxt object
        assets: list of coins in the asset

    Returns:
        assets with new data
    """
    for symbol, data in assets.items():
        # get historical trades list
        trade_info = exchange.fetch_my_trades(symbol + "/USDT")

        trade_value = trade_value_calculator(trade_info)

        assets[symbol]['trade_value'] = trade_value

        # TODO: average price should be calculate
        assets[symbol]['trade_price'] = trade_info[-1]['price']

    return assets


def pnl_info_adder(assets):
    """
    calculate pnl and percent of pnl for every coin in assets

    Args:
        assets: list of coins in the asset

    Returns:
        assets with new data
    """
    for symbol, data in assets.items():
        # pnl = ( current value in $ ) - (trade value in $ )
        assets[symbol]['pnl'] = float("{:.4f}".format(data['current_value'] - data['trade_value']))

        # %pnl = ( pnl * 100 ) / (trade value in $ )
        assets[symbol]['pnl_percent'] = float("{:.4f}".format((assets[symbol]['pnl'] * 100) / data['trade_value']))

    return assets


def calculate_total_info(assets, USDT_amount):
    """
    calculate total value based on all assets PNL

    Args:
        assets: list of coins in the asset
        USDT_amount: free cash

    Returns:
        total_pnl: portfolio total pnl
        total_pnl_percent: percent of total pnl
        portfolio_value: sum of all you have in portfolio

    """
    total_pnl = 0
    total_pnl_percent = 0
    portfolio_value = 0

    for symbol, data in assets.items():
        total_pnl += data['pnl']
        total_pnl_percent += data['pnl_percent']
        portfolio_value += data['current_value']

    # portfolio value = (sum of all assets value in $) + (free cash)
    portfolio_value = float("{:.4f}".format(portfolio_value + USDT_amount))

    # round numbers
    total_pnl = float("{:.4f}".format(total_pnl))
    total_pnl_percent = float("{:.4f}".format(total_pnl_percent))

    return total_pnl, total_pnl_percent, portfolio_value


def assets_info(exchange):
    """
    check binance balance and report assets

    Args:
        exchange: ccxt object

    Returns:
        assets list
    """
    assets = {}
    account_info = exchange.fetch_balance()
    all_balances = account_info['info']['balances']

    # all free assets
    for balance in all_balances:
        if float(balance['free']) != 0:
            assets[balance['asset']] = {'amount': account_info[balance['asset']]['free']}

    free_cash = assets['USDT']['amount']
    assets.pop('USDT', None)

    return assets, free_cash


def pretty_printer(assets, total_pnl, total_pnl_percent, portfolio_value):
    """
    use PrettyTable and colorama to print everything beautifully

    Args:
        assets: list of coins in the asset
        total_pnl: portfolio total pnl
        total_pnl_percent: percent of total pnl
        portfolio_value: sum of all you have in portfolio

    Returns:
        None
    """

    # logo
    logo = pyfiglet.figlet_format("Binance PNL", font="bubble")
    print(Fore.YELLOW + logo)

    # assets report
    coin_table = PrettyTable(['', 'Symbol', 'PNL', '%PNL'])

    for symbol, data in assets.items():

        if data['pnl'] >= 0:

            coin_table.add_row(
                [Fore.GREEN + "●" + Style.RESET_ALL, Fore.WHITE + Style.BRIGHT + symbol + Style.RESET_ALL,
                 Fore.GREEN + Style.BRIGHT + '+' + str(data['pnl']) + ' $' + Style.RESET_ALL,
                 Fore.GREEN + Style.BRIGHT + '+' + str(data['pnl_percent']) + ' %' + Style.RESET_ALL])

        else:

            coin_table.add_row([Fore.RED + "●" + Style.RESET_ALL, Fore.WHITE + Style.BRIGHT + symbol + Style.RESET_ALL,
                                Fore.RED + Style.BRIGHT + str(data['pnl']) + ' $' + Style.RESET_ALL,
                                Fore.RED + Style.BRIGHT + str(data['pnl_percent']) + ' %' + Style.RESET_ALL])

    print(coin_table)
    print(Fore.WHITE + Style.DIM + "++++++++++++++++++++++++++++++++++++++")

    # total report
    if total_pnl >= 0:
        print('Total PNL ................ ', Fore.GREEN + '+' + str(total_pnl) + ' $' + Style.RESET_ALL)
    else:
        print('Total PNL ................ ', Fore.RED + str(total_pnl) + ' $' + Style.RESET_ALL)

    if total_pnl_percent >= 0:
        print('Total %PNL ............... ', Fore.GREEN + '+' + str(total_pnl_percent) + ' %' + Style.RESET_ALL)
    else:
        print('Total %PNL ............... ', Fore.RED + str(total_pnl_percent) + ' %' + Style.RESET_ALL)

    print('Portfolio Value .......... ', Style.DIM + str(portfolio_value) + ' $' + Style.RESET_ALL)


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

    # print data in proper format
    pretty_printer(assets, total_pnl, total_pnl_percent, portfolio_value)
