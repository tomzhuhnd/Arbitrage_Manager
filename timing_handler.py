import time

class TimerHandler:

    def __init__(self):

        self.current_timestamp = None
        self.duration_unit     = None
        self.duration_unit_div = None
        self.duration_length   = None
        self.duration_interval = None

    # Setting functions

    def set_timestamp(self):

        self.current_timestamp = time.time()

    def set_timer_settings(self, duration_unit, duration_length):

        self.duration_unit = duration_unit
        self.duration_length = duration_length

        if duration_unit == 'second':
            self.duration_unit_div = 1

        elif duration_unit == 'minute':
            self.duration_unit_div = 60

        elif duration_unit == 'hour':
            self.duration_unit_div = 60 * 60

        self.duration_interval = self.duration_unit_div * self.duration_length

    # Logic functions

    def check_timer(self):

        if self.current_timestamp is None:
            self.set_timestamp()
            return True, 0

        time_diff = divmod((time.time() - self.current_timestamp), self.duration_interval)

        if time_diff[0] > 0:
            return True, time_diff[1]
        else:
            return False, time_diff[1]
