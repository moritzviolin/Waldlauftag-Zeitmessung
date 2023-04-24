import os
import datetime


# Der Logger kann so benutzt werden:
'''
# Wenn ein Lauf gestartet wird
logger.log_run_started(run_id)

# Wenn ein Lauf beendet wird
logger.log_run_ended(run_id)

# Wenn ein Lauf zurückgesetzt wird
logger.log_run_reset(run_id)

# Wenn ein Läufer ankommt
logger.log_runner_arrived(runner_id)
'''


class Logger:
    def __init__(self, logfile):
        self.log_filename = os.path.join("logs", logfile + ".log")
        os.makedirs(os.path.dirname(self.log_filename), exist_ok=True)
        self.write_line("--------------------------------")
        self.log("Waldlauf-Programm gestartet.")
        self.write_line("--------------------------------")


    def log(self, message):
        with open(self.log_filename, "a", encoding="utf-8") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] {message}\n")


    def write_line(self, message):
        with open(self.log_filename, "a", encoding="utf-8") as file:
            file.write(f"{message}\n")



    def log_run_started(self, run_id):
        message = f"Lauf {run_id} gestartet"
        self.write_line("")
        self.log(message)


    def log_run_resume(self, run_id):
        message = f"Lauf {run_id} wurde aus dem Backup geladen und wird fortgeführt"
        self.write_line("")
        self.log(message)


    def log_run_ended(self, run_id):
        message = f"Lauf {run_id} beendet"
        self.write_line("")
        self.log(message)


    def log_not_arrived_runners(self, runners):
        for r in runners:
            message = "Nicht angekommen: " + str(r[1]) + ", " + r[2] + " (" + str(r[0]) + ")"
            self.log(message)


    def log_run_reset(self, run_id):
        message = f"Lauf {run_id} zurückgesetzt"
        self.write_line("")
        self.log(message)


    def log_runner_arrived(self, runner_id, run_id=-1):
        if run_id == -1:
            message = f"Läufer {runner_id} ist angekommen"
        else:
            message = f"Läufer {runner_id} ist im Lauf {run_id} angekommen"
        self.log(message)
