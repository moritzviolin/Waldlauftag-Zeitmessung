import os
import io
import glob
import datetime, time
from datetime import datetime
from utils import Logger
from utils.say_numbers import say_number
import threading


from utils import utils
# from lib.model.database import Database
from model.db import Database
# from model import config
# from model.settings import Settings

class Data():

    timeformat = "%H:%M:%S"
    base_name = "waldlauf-" + str(datetime.today().year)
    db_name = os.path.join("data", base_name + ".db")
    if not os.path.exists(db_name):
        print("Datenbank " + db_name + " nicht gefunden. Datenbank wird erstellt...")
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
    else:
        print("Datenbank " + db_name + " gefunden.")
    folder_results = "ergebnisse"

    def __init__(self, settings):
        self.logger = Logger(self.base_name)
        self.settings = settings
        self.db = Database(self.db_name)
        self.db.set_resultfolder(self.folder_results)
        self.db.create_runners_table()
        self.db.create_runs_table()
        self.db.insert_run(self.settings.RUN_3, self.settings.RUN_3_NAME)
        self.db.insert_run(self.settings.RUN_5_1, self.settings.RUN_5_1_NAME)
        self.db.insert_run(self.settings.RUN_5_2, self.settings.RUN_5_2_NAME)
        self.db.insert_run(self.settings.RUN_10, self.settings.RUN_10_NAME)
        # self.read_lauf_files()

    # ==========================================================================
    # === Starten und Stoppen

    def starte_lauf(self, run_id):
        # nur die Läufer des Runs in lst_running packen!
        # timestamp = datetime.now()
        timestamp = datetime.now()
        self.db.set_start(run_id, timestamp)
        self.logger.log_run_started(run_id)
        # im Infofile wird die Startzeit gespeichert.
        # diese kann dann nochmal geladen werden, falls das Programm abstürzt
        self.write_infofile()
        return timestamp


    def resume_lauf(self, run_id, timestamp):
        # nur die Läufer des Runs in lst_running packen!
        self.db.set_start(run_id, timestamp)
        self.logger.log_run_resume(run_id)
        # im Infofile wird die Startzeit gespeichert.
        # diese kann dann nochmal geladen werden, falls das Programm abstürzt
        self.write_infofile()


    def stop_run(self, run_id):
        timestamp = datetime.now()
        self.db.set_end(run_id, timestamp)
        # im Infofile wird die Startzeit gespeichert.
        # diese kann dann nochmal geladen werden, falls das Programm abstürzt
        self.write_infofile()
        self.write_data(True)
        self.logger.log_run_ended(run_id)
        not_arrived_runners = self.db.get_not_arrived_runners(run_id)
        self.logger.log_not_arrived_runners(not_arrived_runners)
        return timestamp

    # ==========================================================================

    # ==========================================================================
    # === Läufe verwalten

    def arrived(self, id):
        return_value = 0
        if self.is_running(id):
            if self.settings.SAYNUMBERS:
                try:
                    threading.Thread(target=say_number, args=(str(id), )).start()
                except Exception as err:
                    print(f"Fehler: {err}")
            self.db.arrived(id)
            self.logger.log_runner_arrived(id)
            return_value = 1
        else:
            if self.is_arrived(id):
                return_value = self.settings.MSG_TN_SCHON_ANGEKOMMEN
            elif self.is_teilnehmer(id):
                return_value = self.settings.MSG_TN_NICHT_GESTARTET # "Teilnehmer ist nicht gestartet"
            else:
                return_value = self.settings.MSG_TN_UNBEKANNT #"Teilnehmer unbekannt"
        return return_value


    def reset_run(self, run_id):
        self.db.reset_run(run_id)
        self.logger.log_run_reset(run_id)


    def contains_runners(self):
        return self.db.contains_runners()



    def is_teilnehmer(self, id):
        return self.db.get_runner_by_id(id) != None


    def is_running(self, runner_id):
        # true, wenn der Läufer mit der runner_id gerade läuft
        return self.db.is_runner_running(runner_id) and not self.db.is_arrived(runner_id)


    def is_arrived(self, id):
        return self.db.is_arrived(id)


    def find_teilnehmer(self, id):
        return self.db.get_runner_by_id(id)


    def add_participant(self, tn):
        self.db.insert_runner(tn['id'], tn['nachname'], tn['vorname'], tn['geschlecht'], tn['klasse'], tn['jahrgang'], tn['lauf'])
        # self.lst_alle.append(teilnehmer)


    def get_teilnehmer_from_run(self, run_id):
        return self.db.get_all_runners_from_run(run_id)


    def get_angekommen(self):
        list = []
        for tn in self.lst_alle:
            if tn:
                if str(tn['zeit']) != "0":
                    list.append(tn)
        return list


    def run_is_finished(self, run_id):
        return self.db.run_is_finished(run_id)


    def run_is_active(self, run_id):
        return self.db.run_is_active(run_id)


    def get_running(self, run_id):
        return self.db.get_not_arrived_runners(run_id)


    # =============================================================================
    # === read und write

    def read_data(self):
        """
        Liest die Daten aus einer .csv-Datei in das Programm ein
        Datei soll dem Aufbau folgen: Teilnehmernummer, Nachname, Vornahme, Geschlecht, Jahrgang, Lauf
        """
        self.db.read_runners(self.settings.DATAFILE)


    def find_lauf_files(self):
        # Wenn es bereits Dateien mit Läufe(r)n gibt, können diese eingelesen werden.
        # Die letzte Laufdatei kann geladen werden
        found_not_finished_runs = False
        runs = self.read_info()
        # die ersre Zeile auslassen, weil die die Überschriften enthält
        if runs:
            for r in runs[1:]:
                run_id = r[0]
                latest_file = self.get_latest_file_for_run(run_id)
                if latest_file:
                    # Wenn nur Läufe geladen werden sollen, die noch nicht beendet wurden, muss die zweite Abfrage mit rein
                    # So werden alle Läufe geladen, die gestartet wurden
                    if str(r[1]) != "0": # and str(r[2]) == "0":
                        found_not_finished_runs = True
                        r.append(latest_file)
                '''
                else:
                    print("No file found for run {}" .format(run_id))
                '''
        # wenn eine Datei gefunden wurde, prüfen, ob der Lauf schon beendet wurde
        if found_not_finished_runs:
            return runs


    def get_latest_file_for_run(self, run_id):
        folder_path = self.folder_results
        latest_file = None
        latest_time = datetime.min
        for filename in os.listdir(folder_path):
            if filename.startswith("lauf-{}_".format(run_id)) and filename.endswith(".csv"):
                laufname = "lauf-" + str(run_id)
                parts = filename[len(laufname):].split("_")
                if len(parts) >= 3:
                    date_str = parts[1]
                    time_str = parts[2].replace(".csv", "")
                    try:
                        file_time = datetime.strptime(f"{date_str}_{time_str}", "%Y-%m-%d_%H-%M-%S")
                        if file_time > latest_time:
                            latest_time = file_time
                            latest_file = filename
                    except ValueError:
                        pass
        return latest_file


    def load_backup(self, filename, run_id):
        # Datei mit allen Läufern eines Laufes
        self.db.read_runners_from_backup(os.path.join(self.folder_results, filename), run_id)


    def read_info(self):
        try:
            if not os.path.exists(self.settings.INFOFILE):
                print("Keine Infodatei " + self.settings.INFOFILE + " gefunden. Wird erstellt...")
                os.makedirs(os.path.dirname(self.settings.INFOFILE), exist_ok=True)
            infofile = io.open(self.settings.INFOFILE, mode="r", encoding="utf-8")
            raw_data = infofile.read().rstrip()
            zeilen = raw_data.split("\n")
            runs = []
            if len(zeilen) > 1:
                for zeile in zeilen:
                    rundata = zeile.split(self.settings.SEP) # Den Seperator hier ändern, falls ein anderes CSV-Format verwendet wird
                    run_id = rundata[0]
                    start =  rundata[1]
                    end = rundata[2]
                    runs.append(rundata)
                return runs
        except FileNotFoundError:
            return False
        return False


    # wenn writeresults = True ist, sollen die Ergebnisse final gespeichert werden:
    def write_data(self, writeresults=False):
        if(not writeresults):
            print("autosaving.")
        else:
            print("Daten werden gespeichert.")
        # Die Läufer-Daten aus der Datenbank in eine csv-Datei schreiben.
        self.db.save_runners()
        if (writeresults):
            self.db.save_results()


    def write_infofile(self):
        file_name = self.settings.INFOFILE
        self.db.write_infofile(file_name)



    # ==========================================================================
    # === Helper

    def calc_runtime(self, run_id, timestamp):
        start = 0
        for r in self.runs:
            if r['id'] == run_id:
                start = r['start']
                break
        if start != 0:
            diff = timestamp - start
            return diff
        return 0


    def log(self, text):
        pass
