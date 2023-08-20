#!/usr/bin/env python3
# coding=utf-8

# <bitbar.title>Okx Spot Market</bitbar.title>
# <bitbar.version>1.0.0</bitbar.version>
# <bitbar.author>yvvw</bitbar.author>
# <bitbar.author.github>yvvw</bitbar.author.github>
# <bitbar.desc>Show Okx spot market price.</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

import os
from datetime import datetime
from os import path

import dotenv
import requests
from okx.MarketData import MarketAPI

import util

dotenv.load_dotenv()

OKX_ACCESS_KEY = os.getenv('OKX_ACCESS_KEY')
OKX_SECRET_KEY = os.getenv('OKX_SECRET_KEY')
OKX_PASSPHRASE = os.getenv('OKX_PASSPHRASE')
DEBUG = os.getenv('DEBUG') == 'true'

COINS = os.getenv('OKX_SPOT_MARKET_COINS').split(',')
URL = 'https://www.okx.com/cn/markets/explore'
ETHS_ORDER_HISTORY_API = "https://www.etch.market/api/markets/history/orders?category=token&events=sold&collection=erc-20%20eths&page.size=20&page.index=1"


def main():
    # Show okx spot market price.
    # https://www.okx.com/docs-v5/zh/#rest-api-market-data-get-tickers
    market = MarketAPI(
        api_key=OKX_ACCESS_KEY,
        api_secret_key=OKX_SECRET_KEY,
        passphrase=OKX_PASSPHRASE,
        flag="0",
        debug=DEBUG
    )
    tickers = market.get_tickers(instType='SPOT')['data']
    tickers = list(filter(lambda it: it['instId'] in COINS, tickers))
    tickers.sort(key=lambda it: COINS.index(it['instId']))

    if len(tickers) == 0:
        print(f"no ticker|href={URL}")
        return

    contents = []
    for it in tickers:
        coin = it['instId'].split('-')[0]
        last_price = float(it['last'])
        base_price = float(it['sodUtc0'])
        percent = (last_price - base_price) / base_price
        formatted_utc8_percent = '{:.2%}'.format(percent)

        content = f"{coin} {it['last']} {formatted_utc8_percent}"
        contents.append(content)

    if 'ETHS-USDT' in COINS:
        eths_price_usd = get_eths_price_usd()
        contents.append(f" ETHS {eths_price_usd}")

    print(" ".join(contents) + f"|href={URL}")


def get_eths_price_usd():
    response = requests.get(ETHS_ORDER_HISTORY_API)
    data = response.json()
    event = data['data']['events'][0]
    price_usd = float(event['priceUsd'])
    elapsed = datetime.timestamp(datetime.now()) - datetime.timestamp(datetime.fromtimestamp(event['eventTime']))
    elapsed = "{:.0f}m{:.0f}s".format(elapsed / 60, elapsed % 60) if elapsed >= 60 else "{:.0f}s".format(elapsed)
    return '{:.2f}({})'.format(price_usd, elapsed)


if __name__ == '__main__':
    try:
        util.retry(3, main)
    except Exception as err:
        print(path.basename(os.getenv('SWIFTBAR_PLUGIN_PATH', __file__)) + ': ' + str(err))
