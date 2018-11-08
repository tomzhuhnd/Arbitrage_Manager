# Import general libraries
import time
import json, requests

# Import multi-threading libraries
from threading import Thread, Event

# Import configuration
import connectivity_bfx_config as config

class bfx_webservice(Thread):

    def __init__(self, parent):

        self.name = 'bfx'
        self.type = 'webservice'

        print('Thread: {:<10} - '.format(self.name) + 'Initializing ... ', end='')

        # Class variables
        self.parent = parent
        self.loop_timer = 5

        # Class events
        self._stopped = Event()

        print('Done.')
        super(bfx_webservice, self).__init__()

    def run(self):

        print('Thread: {:<10} - '.format(self.name) + 'Started.')

        # Main loop
        while not self._stopped.is_set():


            time.sleep(self.loop_timer)

        return

    def request_trading_orderbook(self, to_currency, from_currency):

        target_pair = (to_currency.upper(), from_currency.upper())

        request_url = config.bfx_url + 'book/t' + to_currency.upper() + from_currency.upper() + '/P0'
        resp = requests.get(request_url)

        try:
            if resp.status_code != 200:
                print(resp.status_code)
                return
            else:
                orderbook = json.loads(resp.content.decode('utf-8'))

            return orderbook, target_pair

        except Exception as e:
            print('Thread: {:<10} - '.format(self.name) + ' Exception on trading orderbook request: ' + str(e))


    def standardize_orderbook(self, orderbook):

        bids_book = {}
        asks_book = {}

        for level in orderbook['bids']:
            bids_book[float(level['price'])] = float(level['amount'])
        for level in orderbook['asks']:
            asks_book[float(level['price'])] = float(level['amount'])

        orderbook = {'asks': asks_book, 'bids': bids_book}

        return orderbook


    def stop(self):

        print('Thread: {:<10} - '.format(self.name) + 'Shutting down.')
        self._stopped.set()
