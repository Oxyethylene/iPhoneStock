import json
import os
import sys
import time
from json import JSONDecodeError

import requests

STOCK_TYPE_TEMPLATE = \
    'https://www.apple.com.cn/shop/fulfillment-messages?pl=true&mt=compact&parts.0={}&searchNearby=true&store=R639'

CODE_13_PRO = 'MLTE3CH/A'

CODE = CODE_13_PRO


def get_json_from_server(url: str):
    res = requests.get(url)
    try:
        res_json = res.json()['body']['content']['pickupMessage']['stores']
    except JSONDecodeError as e:
        print(f'{time.asctime()}: error while parsing result, result is "{res.text}"')
        raise e

    return res_json


def update_stock(url: str, sleep_time: int):
    while True:
        try:
            stores = get_json_from_server(url)
        except ConnectionError:
            print(f'{time.asctime()}: got connection error, sleep for 10s')
            time.sleep(10)
            continue
        found = False
        for store in stores:
            if store['storeName'] == '深圳益田假日广场':
                continue
            if store['partsAvailability'][CODE]['pickupSearchQuote'] != '暂无供应':
                os.system('say "stock found"')
                found = True
                store_name = store['storeName']
                print(f'{time.asctime()}: stock found at {store_name}')
        if not found:
            print(f'{time.asctime()}: stock not found')
        time.sleep(sleep_time)


def main():
    url = STOCK_TYPE_TEMPLATE.format(CODE)
    try:
        update_stock(url, 5)
    except Exception as e:
        os.system('say "got unexpected exception"')
        print(f'{time.asctime()}: got unexpected exception')
        print(f'{time.asctime()}: {e.with_traceback()}')


if __name__ == '__main__':
    main()
