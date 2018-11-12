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

    def __init__(self, command_queue):

        # Class name
        self._label = 'GUI'
        self._type = 'Manager'
        self._iden = '[' + self._type + ': ' + self._label + ']'

        print('Thread: {:<25} - '.format(self._iden) + 'Initializing ... ', end='')

        # Class events
        self._stopped = Event()

        # Command handlers and variables for interacting with the ProgramManager
        self.command_handlers = {
            'stop program': self.send_stop_program
        }
        self.command_queue = command_queue

        print('Done.')
        super(FrontEndManager, self).__init__()

    def run(self):

        print('Thread: {:<25} - '.format(self._iden) + 'Started.')

        # Generate tkinter master window
        self.gui_root = tk.Tk()

        # Instantiate window classes
        self.window_control = WindowControl(self.gui_root, self.command_handlers)

        self.window_pricing_widget = tk.Toplevel(self.gui_root)
        self.window_pricing        = WindowPricingView(self.window_pricing_widget)

        self.gui_root.after(0, self.run_gui)
        self.gui_root.mainloop()

    def run_gui(self):

        # Gui main loop
        if not self._stopped.is_set():

            self.gui_root.update()

            time.sleep(0.1)

            self.gui_root.after(0, self.run_gui)
        else:
            self.gui_root.destroy()
            self.gui_root.quit()

    def stop_thread(self):
        # Set Stop event
        print('Thread: {:<25} - '.format(self._iden) + 'Stopping thread.')
        self._stopped.set()

    # --------------------------------- Commands to program manager --------------------------------- #

    def send_stop_program(self):

        self.command_queue.put(('stop program', None))


class WindowControl:

    def __init__(self, gui_root, command_handlers):

        # Class internal variables
        self._label = 'Control Window'
        self._type = 'Front End'

        # Tkinter GUI Master root variables
        self.gui_root = gui_root
        self.gui_root.title('Program')
        self.frame = tk.Frame(self.gui_root)
        self.command_handlers = command_handlers

        # Window grid objects
        self._window_grid_obj = {
            0: {0: None}
        }

        # Window grid variables
        self._window_grid_var = {
            0: {0: 'Stop Main Program'}
        }

        # ------------------------------- GUI Elements ------------------------------- #

        self._window_grid_obj[0][0] = tk.Button(
            self.gui_root,text=self._window_grid_var[0][0], background='light grey',
            command=self.__button_stop_program
        )
        self._window_grid_obj[0][0].grid(row=0, column=1, padx=5, pady=5, sticky=('N','W','S','E'), columnspan=1)

    def __button_stop_program(self):
        self.command_handlers['stop program']()

class WindowPricingView:

    def __init__(self, gui_root):

        # Class internal variables
        self._label = 'Pricing View'
        self._type = 'Front End'

        # Tkinter GUI Master root variables
        self.gui_root = gui_root
        self.gui_root.title('Exchange Pricing')
        self.frame = tk.Frame(self.gui_root)
