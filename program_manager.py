# Import generic packages
import time

# Import multi-threading libraries
from multiprocessing import Queue
from threading       import Thread, Event

# Program packages
import front_end_manager
import connectivity_qcx
import timing_handler

class ProgramManager(Thread):

    def __init__(self):

        # Class name
        self._name = 'Program'
        self._type = 'Manager'
        self._iden = '[' + self._type + ': ' + self._name + ']'

        print('Thread: {:<25} - '.format(self._iden) + 'Initializing ... ', end='')

        # Internal variables

        # Internal thread variables
        self._thread_front_end = None
        self._thread_connectivity_qcx = None
        self._thread_list = []

        # Class timers
        self.__timer = timing_handler.TimerHandler()
        self.__timer.set_timer_settings('second', 1)
        self.__sleep = 0.05

        # Queues
        self.command_queue = Queue()

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

        # -------------------------- Threads Initialization -------------------------- #
        # Gui Thread
        self._thread_front_end = front_end_manager.FrontEndManager(self.command_queue)
        self._thread_front_end.start()
        self._thread_list.append(self._thread_front_end)

        # Connectivity Threads #
        # QCX
        self._thread_connectivity_qcx = connectivity_qcx.ConnectivityQCX()
        self._thread_connectivity_qcx.start()
        self._thread_list.append(self._thread_connectivity_qcx)

        print('Thread: {:<25} - '.format(self._iden) + 'Child Thread Initialization complete.')

        #  ------------------------------- MAIN LOOP ------------------------------- #
        while not self.stopped.is_set():

            #  -------------------------- Timed Code -------------------------- #
            time_cond, waited_duration = self.__timer.check_timer()

            # Time waited is too short, skip to next iteration
            if not time_cond:
                time.sleep(self.__sleep)
                continue

            if not self.command_queue.empty():
                command, payload = self.command_queue.get()
                if payload is None:
                    self.command_handlers[command]()
                else:
                    self.command_handlers[command](payload)

            # Reset timer
            self.__timer.set_timestamp()
            # ----------------------------------------------------------------- #
        #  ------------------------------------------------------------------------- #

        # Stop main has been triggered. Shut down all child threads.
        if self.stopped.is_set():
            for thread in self._thread_list:
                thread.stop_thread()

    def stop_program(self):

        print('Thread: {:<25} - '.format(self._iden) + 'Program stop triggered! Shutting down threads.')
        self.stopped.set()


