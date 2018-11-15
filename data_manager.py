# Import generic packages
import time
import timing_handler

# Import multi-threading libraries
from multiprocessing import Queue
from threading import Thread, Event


class DataManager(Thread):

    def __init__(self):

        # Class name
        self._label = 'Data'
        self._type = 'Manager'
        self._iden = '[' + self._type + ': ' + self._label + ']'

        print('Thread: {:<25} - '.format(self._iden) + 'Initializing ... ', end='')

        # Class event flags
        self._stopped = Event()

        # Class timers
        self.__idle_limit = 10
        self.__idle_count = 0
        self.__idle_state = False
        self.__sleep = 0.05

        # Data Queue
        self.data_queue = Queue()

        # Data Grids
        self.__data_grid_order_books = {}

        # Function list
        self.__command_list = {
            'order book': {
                'add exchange': self.order_book_add_exchange,
                'update'      : self.order_book_update_data
            }
        }

        # Temporary
        self.counter = 0
        self.counter_bool = True

        # Initialization done, create thread instance
        super(DataManager, self).__init__()
        print('Done')

    def run(self):

        print('Thread: {:<25} - '.format(self._iden) + 'Started.')

        #  ------------------------------- MAIN LOOP ------------------------------- #
        while not self._stopped.is_set():

            # if self.counter == 200 and self.counter_bool:
            #     self.counter_bool = False
            #     for exchange in self.__data_grid_order_books:
            #         print(exchange)
            #         for orderbook in self.__data_grid_order_books[exchange]:
            #             print('\t' + str(orderbook) + ": " + str(self.__data_grid_order_books[exchange][orderbook])[0:80])

            if not self.data_queue.empty():

                data_grid, command, payload = self.data_queue.get()

                if payload is None:
                    self.__command_list[data_grid][command]()
                else:
                    self.__command_list[data_grid][command](*payload)

                self.__idle_state = False

            elif self.__idle_state:
                time.sleep(self.__sleep)
                self.counter += 1           # Temporary
            else:
                if self.__idle_count == self.__idle_limit:
                    self.__idle_count = 0
                    self.__idle_state = True
                else:
                    self.__idle_count += 1

        #  ------------------------------------------------------------------------- #

    def stop_thread(self):

        # Set stop event
        print('Thread: {:<25} - '.format(self._iden) + 'Stopping thread.')
        self._stopped.set()

    # ============================== Order book functions ============================== #

    def order_book_add_exchange(self, exchange, pair_list):

        self.__data_grid_order_books[exchange] = {}

        for pair in pair_list:

            self.__data_grid_order_books[exchange][pair] = None

        print('Thread: {:<25} - '.format(self._iden) + 'Order book data grid initialized for: ' + str(exchange))

    def order_book_remove_exchange(self, exchange):

        if exchange in self.__data_grid_order_books:
            self.__data_grid_order_books.pop(exchange)
        else:
            pass

    def order_book_update_data(self, exchange, pair, data):

        self.__data_grid_order_books[exchange][pair] = data
