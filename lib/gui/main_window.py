from tkinter import ttk
from tkinter.ttk import *

import tkinter as tk
from tkinter import *
from tkinter import messagebox

import tkinter.font as font

import datetime, time
from datetime import datetime

# from gui.colors import red, red_light, green, green_light, blue, blue_light, yellow, black, white, bg_dark, bg_light, orange
# from gui import colors
# from model import settings

from gui.runpanel import RunPanel
from gui.dialogs import AddParticipantDialog

from utils import utils

class MainWindow(tk.Frame):

    # ============== timer ===============
    elapsed_time_run_3 = 0
    elapsed_time_run_5_1 = 0
    elapsed_time_run_5_2 = 0
    elapsed_time_run_10 = 0

    update_interval = 50 # milliseconds

    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.settings = data.settings
        self.parent = parent
        self.parent.geometry("1920x1080")
        self.parent.title("Zeitmessung Waldlauftag ASG-KL")

        '''
        self.data.settings.large_font = font.Font(size=22, family="Open Sans", weight="bold")
        self.data.settings.mid_font = font.Font(size=16, family="Open Sans", weight="bold")
        self.data.settings.small_font = font.Font(size=12, family="Open Sans")
        self.data.settings.btn_font = font.Font(size=16, family="Open Sans")
        '''
        self.data.settings.large_font = font.Font(size=20, family="Open Sans", weight="bold")
        self.data.settings.mid_font = font.Font(size=13, family="Open Sans", weight="bold")
        self.data.settings.small_font = font.Font(size=11, family="Open Sans", weight="bold")
        self.data.settings.btn_font = font.Font(size=11, family="Open Sans", weight="bold")

        self.textcolor = self.settings.color_text
        self.bg_light =  self.settings.bg_light
        self.bg_dark =  self.settings.bg_dark
        self.bg_input = self.settings.bg_input
        self.color_inactive = self.settings.color_inactive
        self.color_running = self.settings.color_running
        self.color_finished = self.settings.color_finished
        self.color_inactive_light = self.settings.color_inactive_light
        self.color_running_light = self.settings.color_running_light
        self.color_info = self.settings.color_info

        self.config(bg = self.settings.bg_light)

        # Daten
        self.data_exported = True
        self.data_imported = False

        # Sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky='nsw')

        # RunPanels
        # Für jeden Lauf wird ein Runpanel angelegt. Das wird mit der RUN_ID in einem dict gespeichert
        # Alle Runpanels werden im array runpanels gespeichert.
        self.runpanels = []
        runpanel_3 = RunPanel(self, self.settings.RUN_3, self.settings.RUN_3_NAME, [], self.data)
        runpanel_3.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self.runpanels.append({'id': self.settings.RUN_3, 'panel': runpanel_3})

        runpanel_5_1 = RunPanel(self, self.settings.RUN_5_1, self.settings.RUN_5_1_NAME, [], self.data)
        runpanel_5_1.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        self.runpanels.append({'id': self.settings.RUN_5_1, 'panel': runpanel_5_1})

        runpanel_10 = RunPanel(self, self.settings.RUN_10, self.settings.RUN_10_NAME, [], self.data)
        runpanel_10.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        self.runpanels.append({'id': self.settings.RUN_10, 'panel': runpanel_10})

        runpanel_5_2 = RunPanel(self, self.settings.RUN_5_2, self.settings.RUN_5_2_NAME, [], self.data)
        runpanel_5_2.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
        self.runpanels.append({'id': self.settings.RUN_5_2, 'panel': runpanel_5_2})

        # Grid-Konfiguration
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.pack(fill="both", expand=True)

        self.set_teilnehmerliste()
        self.load_runs()
        self.save_data(True)
        # ============== keybinds =============
        self.parent.bind('<Return>', self.get_input)
        self.parent.bind("<Button-1>", self.set_focus)

        self.sidebar.entry.focus()

        # Diese Zeilen verkleinern und vergrößern das Fenster einmal.
        # Ansonsten kann man nichts eingeben, wenn ein Backup geladen wurde.
        # Keine Ahnung, warum das so ist. Aber so gehts. Einfach so lassen.
        self.parent.iconify()
        self.parent.wm_state('normal')
        '''
        current_focus = self.focus_get()
        if current_focus:
            print("Der Fokus liegt auf:", current_focus)
        else:
            print("Kein Element hat den Fokus")
        '''

    def show_add_participant_dialog(self):
        dialog = AddParticipantDialog(self, self.data)
        self.parent.wait_window(dialog)
        result = dialog.result
        return result


    def set_teilnehmerliste(self):
        for p in self.runpanels:
            p['panel'].reset_lists()
        if self.data.contains_runners():
            self.sidebar.status_teilnehmer_lbl.config(text = "Teilnehmer importiert", fg = self.color_running)
            self.sidebar.export_btn.config(state="normal")


    def get_runpanel(self, id):
        for p in self.runpanels:
            if p['id'] == id:
                return p
        return None


    def get_input(self, event):
        entered_number = self.sidebar.entry.get()
        self.sidebar.entry.delete(0, tk.END)
        self.arrived(entered_number)
        # self.parent.after(10, self.update_view)


    def set_focus(self, event):
        self.sidebar.entry.focus_set()


    def arrived(self, number):
        # print("entered number: " + number)
        a = self.data.arrived(number)
        if a == 1:
            runner = self.data.db.get_runner_by_id(number)
            self.show_message(number + " angekommen\n\n" + runner[1] + " " + runner[2] + "\nZeit: " + runner[7], self.color_running)
            self.update_runs()
        else:
            if a == self.settings.MSG_TN_NICHT_GESTARTET or a == self.settings.MSG_TN_SCHON_ANGEKOMMEN:
                self.show_message(a, self.color_finished)
            elif a == self.settings.MSG_TN_UNBEKANNT:
                self.show_message(a, self.color_inactive)
            else:
                self.show_message(a)


    def show_message(self, message, color=None):
        if color == None:
            color = self.settings.color_text
        self.sidebar.show_message(message, color)



    def load_runs(self):
        files = self.data.find_lauf_files()
        latest_time = datetime.min
        if files and files != "":
            frage = "Es wurden Läufe gefunden, die nicht \nrichtig beendet wurden: "
            for f in files:
                '''
                run_id = f[0]
                start = f[1]
                end = f[2]
                '''
                frage += "\n"
                if len(f) > 3: # es wurde eine Backup-Datei dazu gefunden
                    filename = f[3]
                    laufname = "lauf-" + str(f[0])
                    parts = filename[len(laufname):].split("_")
                    if len(parts) >= 3:
                        date_str = parts[1]
                        time_str = parts[2].replace(".csv", "")
                        file_time = datetime.strptime(f"{date_str}_{time_str}", "%Y-%m-%d_%H-%M-%S")
                        s = file_time.strftime("%d.%m.%Y um %H:%M:%S")
                        frage += "Lauf " + f[0] + " vom " + s
            frage += "\nSollen die Dateien noch einmal geladen werden?"
            if messagebox.askyesno("Daten Laden", frage):
                for f in files:
                    run_id = f[0]
                    start = f[1]
                    end = f[2]
                    if len(f) > 3: # es wurde eine Backup-Datei dazu gefunden
                        filename = f[3]
                        self.data.load_backup(filename, f[0])
                        # self.data.db.print_runners()

                        start_str = f[1]
                        start_stamp = datetime.strptime(f"{start_str}", "%Y-%m-%d %H:%M:%S.%f") # 2023-04-20 21:40:40.705925
                        panel = self.get_runpanel(run_id)
                        # if end and (end == 0 or end == "0"):
                        if start and start != 0: # or end == "0"):
                            # print(f"Lauf {run_id} wurde gestartet.")
                            self.start_run(run_id, start_stamp)
                            self.data.resume_lauf(run_id, start_stamp)
                            panel['panel'].resume_run(start_stamp)

                        if end and end != 0 and end != "0":
                            # print(f"Lauf {run_id} wurde schon beendet.")
                            end_stamp = datetime.strptime(f"{end}", "%Y-%m-%d %H:%M:%S.%f") # 2023-04-20 21:40:40.705925
                            panel['panel'].load_finished_run(start, end_stamp)

                self.update_runs()


    def update_runs(self):
        # setzt die Listen entsprechend
        runs = self.data.db.get_runs()
        for run in runs:
            run_id = run[0]
            panel = self.get_runpanel(run_id)
            # if self.data.db.run_is_active(run_id):
            panel['panel'].reset_lists()
            if len(self.data.db.get_all_runners_from_run(run_id)) == 0:
                # timestamp = self.data.stop_run(run_id)
                self.finish_run(run_id)


    # ==========================================================================

    def start_run(self, run_id, timestamp):
        if run_id == self.settings.RUN_3:
            self.sidebar.status_3km_lbl.config(text = "läuft", fg = self.color_running)
        elif run_id == self.settings.RUN_5_1:
            self.sidebar.status_5_1km_lbl.config(text = "läuft", fg = self.color_running)
        elif run_id == self.settings.RUN_5_2:
            self.sidebar.status_5_2km_lbl.config(text = "läuft", fg = self.color_running)
        elif run_id == self.settings.RUN_10:
            self.sidebar.status_10km_lbl.config(text = "läuft", fg = self.color_running)


    def reset_run(self, run_id):
        if run_id == self.settings.RUN_3:
            self.sidebar.status_3km_lbl.config(text = "resettet", fg = self.color_info)
        elif run_id == self.settings.RUN_5_1:
            self.sidebar.status_5_1km_lbl.config(text = "resettet", fg = self.color_info)
        elif run_id == self.settings.RUN_5_2:
            self.sidebar.status_5_2km_lbl.config(text = "resettet", fg = self.color_info)
        elif run_id == self.settings.RUN_10:
            self.sidebar.status_10km_lbl.config(text = "resettet", fg = self.color_info)


    def mark_finished_run(self, run_id):
        if run_id == self.settings.RUN_3:
            self.sidebar.status_3km_lbl.config(text = "Beendet", fg = self.color_finished)
        elif run_id == self.settings.RUN_5_1:
            self.sidebar.status_5_1km_lbl.config(text = "Beendet", fg = self.color_finished)
        elif run_id == self.settings.RUN_5_2:
            self.sidebar.status_5_2km_lbl.config(text = "Beendet", fg = self.color_finished)
        elif run_id == self.settings.RUN_10:
            self.sidebar.status_10km_lbl.config(text = "Beendet", fg = self.color_finished)


    def save_data(self, write_final_results):
        self.data.write_infofile()
        self.data.write_data(write_final_results)


    def quit(self):
        if messagebox.askyesno("Programm beenden", "Wollen Sie das Programm wirklich beenden? \nDie Daten werden automatisch gespeichert."):
            self.save_data(True)
            self.data.write_infofile()
            # self.data.close_db()
            self.parent.destroy()

# ==============================================================================
# === Sidebar                                                                ===
# ==============================================================================

class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#EEEEEE")
        self.config(bg = parent.settings.bg_dark)
        self.grid(column = 0, row = 0, rowspan = 2, sticky = tk.NE + tk.SW, padx = 10, pady = 10)
        self.parent = parent
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.settings = parent.data.settings

        self.icon_save = tk.PhotoImage(file="lib/images/save.png")
        self.icon_close = tk.PhotoImage(file="lib/images/close.png")
        self.icon_reload = tk.PhotoImage(file="lib/images/reload.png")
        self.icon_add_person = tk.PhotoImage(file="lib/images/add_person.png")

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 0)
        self.rowconfigure(5, weight = 0)
        self.rowconfigure(6, weight = 0)
        self.rowconfigure(7, weight = 0)
        self.rowconfigure(8, weight = 0)
        self.rowconfigure(9, weight = 1)
        self.rowconfigure(10, weight = 0)
        self.rowconfigure(11, weight = 0)
        self.rowconfigure(12, weight = 0)
        self.rowconfigure(13, weight = 0)

        srow = 0
        textcolor = self.parent.settings.color_text
        bg_light =  self.parent.settings.bg_light
        bg_dark =  self.parent.settings.bg_dark
        color_inactive = self.parent.settings.color_inactive
        color_inactive_light = self.parent.settings.color_inactive_light
        bg_input = self.parent.settings.bg_input
        color_finished = self.parent.settings.color_finished
        color_info = self.parent.settings.color_info
        color_info_light = self.parent.settings.color_info_light
        self.color_running = self.parent.settings.color_running
        color_running_light = self.parent.settings.color_running_light

        self.title_lbl = tk.Label(self, text = f"Waldlauftag {datetime.today().year}\nASG-KL", fg = textcolor, bg = bg_dark, font = self.settings.mid_font, justify="left", anchor="nw")
        self.title_lbl.grid(column = 0, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10, columnspan = 1)

        # aktuelle Uhrzeit
        self.time_label = tk.Label(self, text="", font=("Helvetica", 24), bg=textcolor, fg = bg_dark)
        self.time_label.grid(column = 1, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10, columnspan = 1)

        srow += 1
        self.status_lbl = tk.Label(self, text = "Status:", fg = textcolor, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_lbl.grid(column = 0, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10, columnspan = 2)

        srow += 1
        self.status_teilnehmer_lbl = tk.Label(self, text = "Keine Teilnehmer importiert", fg = color_inactive, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_teilnehmer_lbl.grid(column = 0, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10, columnspan = 2)

        srow += 1
        self.status_3km_lbl_1 = tk.Label(self, text = "3 km:", fg = textcolor, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_3km_lbl_1.grid(column = 0, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10)
        self.status_3km_lbl = tk.Label(self, text = "Inaktiv", fg = color_inactive, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_3km_lbl.grid(column = 1, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10)

        srow += 1
        self.status_5_1km_lbl_1 = tk.Label(self, text = "5.1 km:", fg = textcolor, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_5_1km_lbl_1.grid(column = 0, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10)
        self.status_5_1km_lbl = tk.Label(self, text = "Inaktiv", fg = color_inactive, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_5_1km_lbl.grid(column = 1, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10)

        srow += 1
        self.status_5_2km_lbl_1 = tk.Label(self, text = "5.2 km:", fg = textcolor, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_5_2km_lbl_1.grid(column = 0, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10)
        self.status_5_2km_lbl = tk.Label(self, text = "Inaktiv", fg = color_inactive, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_5_2km_lbl.grid(column = 1, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10)

        srow += 1
        self.status_10km_lbl_1 = tk.Label(self, text = "10 km:", fg = textcolor, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_10km_lbl_1.grid(column = 0, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10)
        self.status_10km_lbl = tk.Label(self, text = "inaktiv", fg = color_inactive, bg = bg_dark, font = self.settings.mid_font, anchor = "w")
        self.status_10km_lbl.grid(column = 1, row = srow, sticky = tk.NE + tk.SW, padx = 10, pady = 10)

        srow += 1
        self.eingabe_lbl = tk.Label(self, text = "Angekommen (Nummer):", bg = bg_dark, fg = textcolor, font = self.settings.btn_font, anchor = "w")
        self.eingabe_lbl.grid(column = 0, row = srow, columnspan = 2, sticky = tk.NE + tk.SW, padx = 10, pady = 10)

        srow += 1
        self.entry = tk.Entry(self, bg = bg_input, fg = textcolor, font = self.settings.btn_font)
        self.entry.grid(column = 0, row = srow, columnspan = 2, sticky = tk.NE + tk.SW, padx = 10, pady = 0)

        srow += 1
        self.message_lbl = tk.Label(self, anchor="nw",bg = bg_dark, fg = textcolor,font = self.settings.mid_font, justify="left")
        self.message_lbl.grid(column = 0, row = srow, columnspan = 2, sticky = tk.NE + tk.SW, padx = 10, pady = 0)

        '''
        # KEIN Suchfeld einbauen! Der Fokus muss immer auf dem Eingabefeld für die Läufernummern bleiben!
        # Dadurch ist eine Eingabe in ein Suchfeld nicht im Hauptfenster möglich.
        srow += 1
        self.search_lbl = tk.Label(self, text = "Suchen:", bg = bg_dark, fg = white, font = self.settings.btn_font, anchor = "w")
        self.search_lbl.grid(column = 0, row = srow, columnspan = 2, sticky = tk.NE + tk.SW, padx = 10, pady = 10)
        srow += 1
        self.search_input = tk.Entry(self, bg = black, fg = white, font = self.settings.btn_font)
        self.search_input.grid(column = 0, row = srow, columnspan = 2, sticky = tk.NE + tk.SW, padx = 10, pady = 0)
        '''

        # === Buttons ===

        srow += 1
        self.hinzufuegen_btn = tk.Button(self, text = "Teilnehmer hinzufügen", bg = color_finished, fg = self.settings.text_buttons, font = self.settings.btn_font, image=self.icon_add_person, compound=tk.LEFT, padx = 10, anchor="w")
        self.hinzufuegen_btn.config(command = self.add_participant)
        self.hinzufuegen_btn.grid(column = 0, row = srow,  columnspan = 2, sticky = "nsew", padx = 10, pady = 25)

        '''
        # braucht man das?
        self.import_btn = tk.Button(self, text = "Erneut importieren", bg = blue, fg = black, font = self.settings.text_buttons, command=self.import_data, image=self.icon_reload, compound=tk.LEFT, padx = 10, anchor="w")
        # self.import_btn.grid(column = 0, row = 11, sticky = tk.NE + tk.SW, padx = 10, pady = 5, columnspan = 2)
        self.import_btn.grid(column = 0, row = 11, sticky = "nsew", padx = 10, pady = 5, columnspan = 2)
        '''

        srow += 1
        self.export_btn = tk.Button(self, text = "Daten speichern", bg = color_info, fg = self.settings.text_buttons, font = self.settings.btn_font, command=self.save_data, image=self.icon_save, compound=tk.LEFT, padx = 10, anchor="w")
        self.export_btn.grid(column = 0, row = srow, sticky = "nsew", padx = 10, pady = 5, columnspan = 2)

        srow += 1
        self.quit_btn = tk.Button(self, text = "Programm beenden", bg = color_inactive, fg = self.settings.text_buttons, font = self.settings.btn_font, command = self.parent.quit, image=self.icon_close, compound=tk.LEFT, padx = 10, anchor="w")
        self.quit_btn.grid(column = 0, row = srow, sticky="nsew", padx = 10, pady = 25, columnspan = 2)

        self.update_time()


    def add_participant(self):
        tn = self.parent.show_add_participant_dialog()
        if tn != None:
            self.parent.data.add_participant(tn)
            self.parent.update_runs()


    def save_data(self):
        self.parent.save_data(True)
        self.show_message("Daten gespeichert", self.color_running)


    def import_data(self):
        self.parent.data.read_data()
        self.parent.set_teilnehmerliste()
        self.show_message("Daten importiert", self.color_running)
        self.parent.update_view()


    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.time_label.after(500, self.update_time)


    def show_message(self, message, color=None):
        if color == None:
            color = self.settings.color_text
        self.message_lbl.config(fg = color)
        self.message_lbl.config(text = message)
        self.after(5000, self.clear_message)


    def clear_message(self):
        self.message_lbl.config(text="")
