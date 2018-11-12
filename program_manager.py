# Import generic packages
import time

# Import multi-threading libraries
from multiprocessing import Queue
from threading       import Thread, Event

# Program packages
import data_manager
import front_end_manager
import connectivity_qcx

class ProgramManager(Thread):

    def __init__(self):

        # Class name
        self._label = 'Program'
        self._type = 'Manager'
        self._iden = '[' + self._type + ': ' + self._label + ']'

        print('Thread: {:<25} - '.format(self._iden) + 'Initializing ... ', end='')

        # Internal thread variables
        self._thread_data_manager = None
        self._thread_front_end = None
        self._thread_connectivity_qcx = None
        self._thread_dict = {}

        # Class timers
        self.__idle_limit = 10
        self.__idle_count = 0
        self.__idle_state = False
        self.__sleep = 0.05

        # Queues
        self.command_queue = Queue()
        self.data_queue = None

        # Class event flags
        self.stopped = Event()

        # Command handlers
        self.command_handlers = {
            'stop program': self.stop_program
        }

        # Initialization done, create thread instance
        super(ProgramManager, self).__init__()
        print('Done.')

    def run(self):

        print('Thread: {:<25} - '.format(self._iden) + 'Initializing and starting child threads: ')

        # ------------------------- Data Grid Initialization ------------------------- #
        self.data_grid = None

        # -------------------------- Threads Initialization -------------------------- #

        # Data Manager Thread
        self._thread_data_manager = data_manager.DataManager()
        self._thread_data_manager.start()
        self.data_queue = self._thread_data_manager.data_queue
        self._thread_dict[1] = self._thread_data_manager

        # Gui Thread
        self._thread_front_end = front_end_manager.FrontEndManager(self.command_queue)
        self._thread_front_end.start()
        self._thread_dict[2] = self._thread_front_end

        # Connectivity Threads #
        # QCX
        self._thread_connectivity_qcx = connectivity_qcx.ConnectivityQCX(self.data_queue)
        self._thread_connectivity_qcx.start()
        self._thread_dict[3] = self._thread_connectivity_qcx

        print('Thread: {:<25} - '.format(self._iden) + 'Child Thread Initialization complete!')

        #  ------------------------------- MAIN LOOP ------------------------------- #
        while not self.stopped.is_set():

            if not self.command_queue.empty():
                command, payload = self.command_queue.get()
                if payload is None:
                    self.command_handlers[command]()
                else:
                    self.command_handlers[command](payload)
                self.__idle_state = False
            elif self.__idle_state:
                time.sleep(self.__sleep)
            else:
                if self.__idle_count == self.__idle_limit:
                    self.__idle_count = 0
                    self.__idle_state = True
                else:
                    self.__idle_count += 1



        #  ------------------------------------------------------------------------- #

        # Stop main has been triggered. Shut down all child threads.
        if self.stopped.is_set():
            for x in range(len(self._thread_dict), 0, -1):
                self._thread_dict[x].stop_thread()

    def stop_program(self):

        print('Thread: {:<25} - '.format(self._iden) + 'Program stop triggered! Shutting down threads.')
        self.stopped.set()


