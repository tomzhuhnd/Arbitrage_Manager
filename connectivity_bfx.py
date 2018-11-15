# Import general libraries
import time
import json, requests
import timing_handler

# Import config
import connectivity_bfx_config as config

# Import multi-threading libraries
from threading import Thread, Event

class ConnectivityBFX(Thread):

    def __init__(self, data_queue):

        # Class name
        self._label = 'BFX'
        self._type = 'Connectivity'
        self._iden = '[' + self._type + ': ' + self._label + ']'

        print('Thread: {:<25} - '.format(self._iden) + 'Initializing ... ', end='')

        # Class variables
        self.pair_list = config.trading_pairs
        self.loop_timer = 60

        # Class timers
        self.__timer = timing_handler.TimerHandler()
        self.__timer.set_timer_settings('minute', 1)
        self.__sleep = 0.1

        # Class events
        self._stopped = Event()

        # Data grid variables
        self.data_queue = data_queue

        # Initialization done, create thread instance
        super(ConnectivityBFX, self).__init__()
        print('Done.')

    def run(self):

        print('Thread: {:<25} - '.format(self._iden) + 'Started.')

        # Initialize in data manager
        self.init_to_data_manager()
        time.sleep(0.5)

        # Main loop
        while not self._stopped.is_set():

            # ------------------------- Timed code ------------------------- #
            time_cond, waited_duration = self.__timer.check_timer()

            if not time_cond:
                time.sleep(self.__sleep)
                continue

            self.load_all_books()

            # Reset timer
            self.__timer.set_timestamp()
            # ----------------------- Timed Code End ----------------------- #

        return

    def stop_thread(self):
        # Set stop event
        print('Thread: {:<25} - '.format(self._iden) + 'Stopping thread.')
        self._stopped.set()

    def init_to_data_manager(self):

        # Add all the pairs to order book data grid
        self.data_queue.put(('order book', 'add exchange', (self._label, self.pair_list)))

    # ============================== Functions ============================== #
    def load_all_books(self):

        for trade_pair in self.pair_list:
            # Request the order book details
            status, pair, payload = request_trading_order_book(trade_pair[0], trade_pair[1])
            if status:
                # TODO: Load order book details into data grid
                self.update_data_grid_order_book(pair, payload)
            else:
                if payload[0] == 'rejection':               # QCX rejected our request
                    print('Thread: {:<25} - '.format(self._iden) +
                          'Request rejected! Reason: ' + str(payload[1]))
                    return
                elif payload[0] == 'request error':         # Network request error
                    print('Thread: {:<25} - '.format(self._iden) +
                          'Network Request Error! Status Code: ' + str(payload[1]))
                    # TODO: This should trigger a stop command | Network
                    return
                elif payload[0] == 'exception':             # Exception came up on the request, should restart
                    print('Thread: {:<25} - '.format(self._iden) +
                          'Exception raised! Exception: ' + str(payload[1]))
                    # TODO: This should trigger a thread restart
                    return

    def update_data_grid_order_book(self, pair, order_book):

        # Send update command to data manager
        self.data_queue.put(('order book', 'update', (self._label, pair, order_book)))

# ==================================== REST functions ==================================== #
def request_trading_order_book(to_currency, from_currency):

    request_url = config.bfx_url + 'book/t' + to_currency.upper() + from_currency.upper() + '/P0'
    # request_parameters = {'len': 100}

    try:
        resp = requests.get(request_url)

        if resp.status_code != 200:
            # Request error, something wrong with the network: will return a status code to diagnose
            return False, (to_currency, from_currency), ('request error', resp.status_code)
        else:
            order_book = json.loads(resp.content.decode('utf-8'))

        # Check if there is an error code in the message
        if 'error' in order_book:
            return False, (to_currency, from_currency), ('rejection', order_book['error'])

        # Successful request, return order book
        return True, (to_currency, from_currency), standardize_order_book(order_book)

    except Exception as e:
        # General exception catch
        return False, (to_currency, from_currency), ('exception', e)


def standardize_order_book(order_book):

    bids_book = {}
    asks_book = {}

    for level in order_book:
        if level[2] > 0:
            bids_book[level[0]] = level[2]
        else:
            asks_book[level[0]] = level[2]

    return {'asks': asks_book, 'bids': bids_book}

# print(request_trading_order_book('BCH', 'BTC'))