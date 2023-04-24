import sqlite3
import csv
import os
import shutil
import datetime, time
from datetime import datetime

class Database:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name,
                                           detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

    # =========================================================================
    # === Tabellen anlegen

    def set_resultfolder(self, resultfolder):
        self.folder_results = resultfolder

    def create_runners_table(self):
        with Database(self.db_name) as cursor:
            cursor.execute("DROP TABLE IF EXISTS runners;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runners (
                    id INTEGER PRIMARY KEY UNIQUE,
                    nachname TEXT,
                    vorname TEXT,
                    geschlecht TEXT,
                    klasse TEXT,
                    jahrgang INTEGER,
                    lauf TEXT,
                    zeit TEXT CHECK(zeit LIKE '__:__:__' OR zeit IS NULL)
                )
            """)


    def create_runs_table(self):
        with Database(self.db_name) as cursor:
            cursor.execute("DROP TABLE IF EXISTS runs;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY UNIQUE,
                    name TEXT,
                    start TIMESTAMP NULL,
                    end TIMESTAMP NULL
                )
            """)

    # =========================================================================

    # =========================================================================
    # === Läufe

    def insert_run(self, run_id, name):
        with Database(self.db_name) as cursor:
            try:
                cursor.execute("""
                    INSERT INTO runs (id, name) VALUES (?, ?)
                """, (run_id, name))
            except sqlite3.IntegrityError:
                print(f"Run with ID {run_id} already exists.")


    # --------------------------------
    # zum Debuggen
    def print_runs(self):
        with Database(self.db_name) as cursor:
            for row in cursor.execute("SELECT * FROM runs"):
                print(row)


    def print_runners(self):
        with Database(self.db_name) as cursor:
            cursor.execute('SELECT * FROM runners ORDER BY zeit')
            result = cursor.fetchall()
            print(f"{len(result)} Läufer:")
            print("-----------------")
            for r in result:
                print(r)
            print()
    # --------------------------------


    def set_start(self, run_id, start):
        with Database(self.db_name) as cursor:
            cursor.execute("""
                UPDATE runs SET start=? WHERE id=?
            """, (start, run_id))


    def set_end(self, run_id, end):
        with Database(self.db_name) as cursor:
            cursor.execute("""
                UPDATE runs SET end=? WHERE id=?
            """, (end, run_id))


    def reset_run(self, run_id):
        with Database(self.db_name) as cursor:
            cursor.execute("UPDATE runs SET start = NULL, end = NULL WHERE id = ?", (run_id,))
            cursor.execute("UPDATE runners SET zeit = NULL WHERE lauf = ?", (run_id,))


    def get_runs(self):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT * FROM runs")
            return cursor.fetchall()


    def run_is_active(self, run_id):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT start, end FROM runs WHERE id = ? AND start IS NOT NULL AND end IS NULL", (run_id,))
            result = cursor.fetchone()
            return result is not None


    def run_has_runners(self, run_id):
        with Database(self.db_name) as cursor:
            # Get the total number of runners for the run
            cursor.execute("SELECT COUNT(*) FROM runners WHERE lauf=?", (run_id,))
            total_runners = cursor.fetchone()[0]
            # Get the number of runners who have arrived
            cursor.execute("SELECT COUNT(*) FROM runners WHERE lauf=? AND zeit IS NOT NULL", (run_id,))
            arrived_runners = cursor.fetchone()[0]

            # Compare the total number of runners with the number of arrived runners
            if arrived_runners < total_runners:
                return True
            else:
                return False


    def run_is_finished(self, run_id):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT start, end FROM runs WHERE id = ? AND start IS NOT NULL AND end IS NOT NULL", (run_id,))
            result = cursor.fetchone()
            return result is not None


    def waldlauf_active(self):
        # True, wenn noch irgendein Lauf aktiv, also noch nicht beendet ist
        with Database(self.db_name) as cursor:
            cursor.execute("""
                SELECT * FROM runs WHERE start IS NOT NULL AND end IS NULL
            """)
            active_runs = cursor.fetchall()
            return len(active_runs) > 0


    def get_first_run_start(self):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT start FROM runs ORDER BY start ASC LIMIT 1")
            first_start = cursor.fetchone()[0]
            if first_start is not None:
                return datetime.strptime(first_start, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
            return ""

    # =========================================================================
    # === Läufer

    def insert_runner(self, id, nachname, vorname, geschlecht, klasse, jahrgang, lauf):
        # print("inserting runner " + str(id) + "  ("+ lauf + ")")
        with Database(self.db_name) as cursor:
            cursor.execute("""
                INSERT INTO runners (id, nachname, vorname, geschlecht, klasse, jahrgang, lauf)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id, nachname, vorname, geschlecht, klasse, jahrgang, lauf))


    def set_runner_time(self, runner_id, time):
        with Database(self.db_name) as cursor:
            cursor.execute("UPDATE runners SET zeit = ? WHERE id = ?", (time, runner_id))


    def set_runner_time(self, id, time):
        with Database(self.db_name) as cursor:
            cursor.execute("""
                UPDATE runners
                SET zeit = ?
                WHERE id = ?
            """, (time, id))


    def arrived(self, runner_id):
        # print(f"DB: Angekommen: {runner_id}")
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT lauf FROM runners WHERE id = ?", (runner_id,))
            run_id = cursor.fetchone()[0]

            cursor.execute("SELECT start FROM runs WHERE id = ?", (run_id,))
            start = cursor.fetchone()[0]

            now = datetime.now()
            time_diff = now - start
            seconds_diff = int(time_diff.total_seconds())
            time_formatted = self.convert_seconds_to_hms(seconds_diff)
            cursor.execute("UPDATE runners SET zeit = ? WHERE id = ?", (time_formatted, runner_id))
            return seconds_diff


    def convert_seconds_to_hms(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"


    def contains_runners(self):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT COUNT(*) FROM runners")
            count = cursor.fetchone()[0]
            return count > 0


    def get_runners(self):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT * FROM runners")
            return cursor.fetchall()


    def get_all_runners_from_run(self, run_id):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT * FROM runners WHERE lauf=?", (run_id,))
            rows = cursor.fetchall()
            return rows


    def get_runner_by_id(self, runner_id):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT * FROM runners WHERE id=?", (runner_id,))
            return cursor.fetchone()


    def get_not_arrived_runners(self, run_id):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT start FROM runs WHERE id = ?", (run_id,))
            start_time = cursor.fetchone()[0]
            cursor.execute("SELECT * FROM runners WHERE lauf = ? AND (zeit IS NULL OR zeit = '')", (run_id,))
            runners = cursor.fetchall()
            not_arrived = []
            for runner in runners:
                if start_time and not runner[7]:
                    not_arrived.append(runner)
                    # print("n/a: " + str(runner))
            return not_arrived


    def get_next_free_id(self):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT MAX(id) FROM runners")
            max_id = cursor.fetchone()[0]
            return max_id + 1


    def get_arrived_runners(self, run_id):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT * FROM runners WHERE lauf=? AND zeit IS NOT NULL ORDER BY zeit", (run_id,))
            rows = cursor.fetchall()
            return rows


    def is_runner_running(self, runner_id):
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT lauf FROM runners WHERE id = ?", (runner_id,))
            run_id = cursor.fetchone()
            if not run_id:
                # kein Eintrag für diesen Läufer in der runners-Tabelle gefunden
                return None
            run_id = run_id[0]
            cursor.execute("SELECT start, end FROM runs WHERE id = ?", (run_id,))
            run_data = cursor.fetchone()
            if not run_data:
                # kein Eintrag für diesen Lauf in der runs-Tabelle gefunden
                return None
            start, end = run_data
            # Läufer ist am Lauf teilnehmend, wenn `start` nicht NULL ist
            return start is not None


    def is_arrived(self, runner_id):
        # True, wenn der Läufer schon angekommen ist
        with Database(self.db_name) as cursor:
            cursor.execute("SELECT zeit FROM runners WHERE id = ?", (runner_id,))
            row = cursor.fetchone()
            if row is not None and row[0] is not None:
                zeit = row[0]
                return True
            else:
                return False


    # ========================================================================
    # === speichern

    def read_runners(self, file_name):
        try:
            with Database(self.db_name) as cursor:
                with open(file_name, newline="", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    # next(reader)  # skip header row
                    for row in reader:
                        if row and str(row) != "":
                            cursor.execute("""
                                INSERT INTO runners (id, nachname, vorname, geschlecht, klasse, jahrgang, lauf)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, row)
        except FileNotFoundError:
            print("""
╔═════════════════════════════════════════╗
║                  Fehler                 ║
║ Keine Datei "daten.csv" wurde gefunden! ║
║                                         ║
╚═════════════════════════════════════════╝
            """)
            exit()

    def read_runners_from_backup(self, file_name, run_id):
        # print("reading backup from " + file_name)
        with Database(self.db_name) as cursor:
            with open(file_name, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # skip header row
                cursor.execute("DELETE FROM runners WHERE lauf=?", (run_id,))
                for row in reader:
                    if row[7] == "":
                        row[7] = None
                    if row and str(row) != "":
                        cursor.execute("""
                            INSERT INTO runners (id, nachname, vorname, geschlecht, klasse, jahrgang, lauf, zeit)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, row)


    def write_infofile(self, file_name, delimiter=","):
        with Database(self.db_name) as cursor:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=delimiter)
                writer.writerow(['id', 'start', 'end'])
                for row in cursor.execute("SELECT id, start, end FROM runs"):
                    run_id, start, end = row
                    if not start:
                        start = 0
                    if not end:
                        end = 0
                    writer.writerow([run_id, start, end])


    def save_runners(self):
        # backup_folder = os.path.join("data", "backup", self.get_first_run_start())
        # os.makedirs(backup_folder, exist_ok=True)
        pass
        '''
        print("DB: save runners")
        with Database(self.db_name) as cursor:
            runs = self.get_runs()
            for run in runs:
                run_id = run[0]
                runners = self.get_all_runners_from_run(run_id)
                filename = os.path.join("data", "lauf-" + str(run_id) + ".csv")
                with open(filename, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["id", "Nachname", "Vorname", "Geschlecht", "Klasse", "Jahrgang", "Lauf", "Zeit"])
                    for runner in runners:
                        writer.writerow(runner)
                        # print(f"saving {runner[0]}: {runner[1]} {runner[2]} - {runner[7]}")
        '''

    # Diese Funktion wird aufgerufen, wenn ein Lauf beendet wurde. Die Ergebnisse werden dann in "ergebnisse/ gespeichert."
    def save_results(self):
        # print("DB: save results")
        with Database(self.db_name) as cursor:
            runs = self.get_runs()
            for run in runs:
                run_id = run[0]
                start = run[2]
                end = run[3]
                if start is not None:
                    # if end and end < datetime.now():
                    runners = self.get_all_runners_from_run(run_id)
                    start_time_str = start.strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"lauf-{run_id}_{start_time_str}.csv"
                    os.makedirs(self.folder_results, exist_ok=True)
                    filepath = os.path.join(self.folder_results, filename)
                    with open(filepath, "w", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(["id", "Nachname", "Vorname", "Geschlecht", "Klasse", "Jahrgang", "Lauf", "Zeit"])
                        for runner in runners:
                            writer.writerow(runner)
