#!/usr/bin/env python3
# coding=utf-8

# <bitbar.title>Okx Balance</bitbar.title>
# <bitbar.version>1.0.0</bitbar.version>
# <bitbar.author>yvvw</bitbar.author>
# <bitbar.author.github>yvvw</bitbar.author.github>
# <bitbar.desc>Show Okx balance.</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

import os
from os import path

import dotenv
from okx.Account import AccountAPI

dotenv.load_dotenv()

OKX_ACCESS_KEY = os.getenv('OKX_ACCESS_KEY')
OKX_SECRET_KEY = os.getenv('OKX_SECRET_KEY')
OKX_PASSPHRASE = os.getenv('OKX_PASSPHRASE')
DEBUG = os.getenv('DEBUG') == 'true'

# Custom show coins.
COINS = os.getenv('OKX_BALANCE_COINS').split(',')
URL = 'https://www.okx.com/cn/balance/overview'


def main():
    # Show Okx balance.
    # https://www.okx.com/docs-v5/zh/#rest-api-account-get-balance
    api = AccountAPI(
        api_key=OKX_ACCESS_KEY,
        api_secret_key=OKX_SECRET_KEY,
        passphrase=OKX_PASSPHRASE,
        flag="0",
        debug=DEBUG
    )
    balances = api.get_account_balance()['data'][0]['details']

    balances = list(filter(lambda _it: _it['ccy'] in COINS, balances))
    balances.sort(key=lambda _it: COINS.index(_it['ccy']))

    if len(balances) == 0:
        print(f"no balance|href={URL}")
        return

    contents = []
    for _it in balances:
        formatted_usd = '{:,.2f}'.format(float(_it['eqUsd']))

        content = f"{_it['ccy']} {formatted_usd}"
        contents.append(content)

    print(" ".join(contents) + f"|href={URL}")


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(path.basename(os.getenv('SWIFTBAR_PLUGIN_PATH', __file__)) + ': ' + str(err))
