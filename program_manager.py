# Import generic packages
import time

# Import multi-threading libraries
from multiprocessing import Queue
from threading       import Thread, Event

# Program packages
import front_end_manager


class ProgramManager(Thread):

    def __init__(self):

        time.sleep(1)

        # Class name
        self._name = 'program'
        self._type = 'manager'
        self._iden = self._name + ' ' + self._type

        print('Thread: {:<10} - '.format(self._iden) + 'Initializing ... ', end='')

        # Internal variables

        # Internal thread variables
        self._thread_front_end = None

        # Class event flags
        self.stopped = Event()

        super(ProgramManager, self).__init__()
        print('Done.')

    def run(self):

        # -------------------------- Threads Initialization -------------------------- #
        # Gui Thread
        self._thread_front_end = front_end_manager.FrontEndManager()
        self._thread_front_end.start()

        # Main loop
        while not self.stopped.is_set():
            
            time.sleep(1)

