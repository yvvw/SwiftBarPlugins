#!/usr/bin/env python3
# coding=utf-8

# <bitbar.title>Okx Position</bitbar.title>
# <bitbar.version>1.0.0</bitbar.version>
# <bitbar.author>yvvw</bitbar.author>
# <bitbar.author.github>yvvw</bitbar.author.github>
# <bitbar.desc>Show Okx position.</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

import os
from os import path

import dotenv
from okx.Account import AccountAPI

import util

dotenv.load_dotenv()

OKX_ACCESS_KEY = os.getenv('OKX_ACCESS_KEY')
OKX_SECRET_KEY = os.getenv('OKX_SECRET_KEY')
OKX_PASSPHRASE = os.getenv('OKX_PASSPHRASE')
DEBUG = os.getenv('DEBUG') == 'true'

URL = 'https://www.okx.com/cn/trade-swap'


def main():
    # Show Okx position.
    # https://www.okx.com/docs-v5/zh/#rest-api-account-get-positions
    api = AccountAPI(
        api_key=OKX_ACCESS_KEY,
        api_secret_key=OKX_SECRET_KEY,
        passphrase=OKX_PASSPHRASE,
        flag="0",
        debug=DEBUG
    )
    positions = api.get_positions()['data']
    positions.sort(key=lambda it: -float(it['upl']))

    if len(positions) == 0:
        print(f"no position|href={URL}")
        return

    contents = []
    for it in positions:
        coin = it['instId'].split('-')[0]
        formatted_gain = '{:,.2f}'.format(float(it['upl']))
        formatted_gain_percent = '{:.2%}'.format(float(it['uplRatio']))

        content = f"{coin} {it['posSide']} {formatted_gain} {formatted_gain_percent}"
        contents.append(content)

    print(" ".join(contents) + f"|href={URL}")


if __name__ == '__main__':
    try:
        util.retry(3, main)
    except Exception as err:
        print(path.basename(os.getenv('SWIFTBAR_PLUGIN_PATH', __file__)) + ': ' + str(err))
