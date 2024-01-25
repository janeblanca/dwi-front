class InputTime:
    def __init__(self, window):
        self.window = window

    def set_break_time(self):
        break_time_str = self.window.user_input_break.text()
        try:
            self.window.break_time = int(break_time_str) * 60
            print(f"Break time set to {self.window.break_time} seconds.")
            self.window.user_input_break.clear()
        except ValueError:
            print("Invalid input. Please enter a valid integer for break time.")

    def set_break_interval(self):
        break_interval_str = self.window.user_input_breakint.text()
        try:
            self.window.break_interval = int(break_interval_str) * 60
            print(f"Break interval set to {self.window.break_interval} seconds.")
            self.window.user_input_breakint.clear()
        except ValueError:
            print("Invalid input. Please enter a valid integer for break interval.")

    def format_time(self, seconds):
        minutes, sec = divmod(seconds, 60)
        return f"{minutes:02d}:{sec:02d}"

    def validate_inputs(self):
        try:
            self.set_break_time()
            self.set_break_interval()

            self.window.original_break_time = self.window.break_time
            self.window.original_break_interval = self.window.break_interval

            self.window.user_input_break.setEnabled(False)
            self.window.user_input_breakint.setEnabled(False)

            self.window.break_interval_active = True
            self.window.start_timer()

        except ValueError:
            print("Invalid input. Please enter valid integers for break time and break interval.")

    def start_timer(self):
        if self.window.break_interval_active:
            if self.window.break_interval > 0:
                self.window.break_interval -= 1

                if self.window.break_interval == 0:
                    self.window.break_interval_active = False
                    self.window.break_time = self.window.original_break_time
                    self.window.show_notification("Take a Break!", "Do Wrist Exercises!")

        else:
            if self.window.break_time > 0:
                self.window.break_time -= 1

                if self.window.break_time == 0:
                    self.window.total_work_time += self.window.original_break_interval
                    self.window.break_interval = self.window.original_break_interval
                    self.window.show_notification("Break Time Over", "Back to work!")

        self.window.update()
