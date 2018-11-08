# Import generic packages
import time
import configparser

# Import multi-threading capacity
from multiprocessing import Queue
from threading import Thread, Event

# Import GUI packages
import tkinter      as tk
import tkinter.font as tkFont
import tkinter.ttk  as ttk

font_collection = {}

class FrontEndManager(Thread):

    def __init__(self):

        # Class name
        self._name = 'gui'
        self._type = 'manager'
        self._iden = self._name + ' ' + self._type

        print('Thread: {:<10} - '.format(self._iden) + 'Initializing ... ', end='')

        # Class variables
        self.loop_timer = 0.05

        # Class events
        self._stopped = Event()

        # Class command handlers
        self.command_handlers = {

        }

        print('Done.')
        super(FrontEndManager, self).__init__()

    def run(self):

        print('Thread: {:<10} - '.format(self._iden) + 'Started.')

        # Generate tkinter master window
        self.gui_root = tk.Tk()

        # Instantiate window classes
        self.main_window = main_window(self.gui_root)

        self.gui_root.after(0, self.run_gui)
        self.gui_root.mainloop()

    def run_gui(self):

        # Gui main loop
        if not self._stopped.is_set():

            self.gui_root.update()
            time.sleep(self.loop_timer)

            self.gui_root.after(0, self.run_gui)
        else:
            # Todo: set all tkinter varaibles to None on exit
            self.gui_root.destroy()
            self.gui_root.quit()

    def stop(self):
        # Set Stop event
        print('Thread: {:<10} - '.format(self._iden) + 'Shutting down.')
        self._stopped.set()


class main_window:

    def __init__(self, gui_root):

        # Class internal variables
        self.__name = 'gui'
        self.gui_root = gui_root
        self.gui_root.title('Program')
        self.frame = tk.Frame(self.gui_root)

        # Window grid objects
        self._window_grid_obj = {
            0: {0: None}
        }

        # Window grid variables
        self._window_grid_var = {
            0: {0: 'Stop Main Program'}
        }

        self._window_grid_obj[0][0] = tk.Button(
            self.gui_root,text=self._window_grid_var[0][0], background='light grey',
            command=self.__stop
        )
        self._window_grid_obj[0][0].grid(row=0, column=1, padx=5, pady=5, sticky=('N','W','S','E'), columnspan=1)

    def __stop(self):

        print('Stop')