from tkinter import ttk
from tkinter.ttk import *

import tkinter as tk
from tkinter import *
from tkinter import messagebox

import tkinter.font as font

import datetime, time
from datetime import datetime

# from gui.colors import red, red_light, green, green_light, blue, blue_light, yellow, black, white, bg_dark, bg_light, orange
from model.settings import Settings
# from gui import colors
# from model import config
from utils import utils


class RunPanel(tk.Frame):

    start_time = 0
    is_running = False
    elapsed_time = 0

    sort_ascending = True

    lauf_aktiv = True
    startzeit = time.time()
    time_str = utils.make_time_str(startzeit)


    def __init__(self, parent, run_id, name, runners, data):
        super().__init__(parent)

        self.parent = parent
        self.name = name
        self.data = data
        self.settings = data.settings
        self.runners = runners
        self.run_id = run_id

        # alle Farben speichern, damit man einfacher drauf zugreifen kann
        self.col_button_start = self.settings.color_running
        self.col_button_start_disabled = self.settings.color_running_light
        self.col_button_end = self.settings.color_inactive
        self.col_button_end_disabled = self.settings.color_inactive_light
        self.col_button_data = self.settings.color_info
        self.color_info = self.settings.color_info
        self.bg_dark = self.settings.bg_dark
        self.bg_light = self.settings.bg_light
        self.color_text = self.settings.color_text
        self.text_buttons = self.settings.text_buttons
        self.color_running = self.settings.color_running
        self.color_running_light = self.settings.color_running_light
        self.color_inactive = self.settings.color_inactive
        self.color_inactive_light = self.settings.color_inactive_light
        self.color_finished = self.settings.color_finished

        self.start_time = 0
        self.is_running = False
        self.elapsed_time = 0
        self.init_gui(name)


    def init_gui(self, name):
        self.config(bg=self.bg_dark)

        # Icons
        self.icon_sort = tk.PhotoImage(file="lib/images/sort_arrows.png")
        self.icon_stop = tk.PhotoImage(file="lib/images/stop.png")
        self.icon_start = tk.PhotoImage(file="lib/images/start.png")

        # Ein Rahmen um das Panel, der je nach Status eine andere Farbe bekommt
        self.config(borderwidth=5, highlightbackground=self.bg_light, highlightthickness=5)

        # ======================================================================
        # Linkes Panel mit Timer und Buttons

        left_panel = tk.Frame(self, bg=self.bg_dark)
        left_panel.grid(column=0, row=0, sticky="n", padx=10, pady=10)

        lrow = 0
        self.title_lbl = tk.Label(left_panel, text=name, fg=self.color_text, bg=self.bg_dark, font=self.settings.large_font, anchor="w")
        self.title_lbl.grid(column=0, row=lrow, sticky=tk.NW, padx=0, pady=0)

        lrow += 1
        self.start_lbl = tk.Label(left_panel, text="Startzeit:", bg=self.bg_dark, fg=self.color_text, font=self.settings.mid_font, anchor="w")
        self.start_lbl.grid(column=0, row=lrow, sticky=tk.NW, padx=0, pady=(10, 0))

        lrow += 1
        self.startzeit_lbl = tk.Label(left_panel, text="00:00:00", bg=self.bg_dark, fg=self.color_text, font=self.settings.large_font, anchor="w")
        self.startzeit_lbl.grid(column=0, row=lrow, sticky=tk.NW, padx=0)

        lrow += 1
        self.aktuelle_lbl = tk.Label(left_panel, text="Laufzeit:", bg=self.bg_dark, fg=self.color_text, font=self.settings.mid_font, anchor="w")
        self.aktuelle_lbl.grid(column=0, row=lrow, sticky=tk.NW, padx=0, pady=(15, 0))

        lrow += 1
        self.aktuelle_zeit_lbl = tk.Label(left_panel, text="00:00:00.00", bg=self.bg_dark, fg=self.color_text, font=self.settings.large_font, anchor="w")
        self.aktuelle_zeit_lbl.grid(column=0, row=lrow, sticky=tk.NW, padx=0)

        # Start und Stop
        bw = 70 # button width
        lrow += 1
        self.start_pause_btn = tk.Button(left_panel, text = "Start", image=self.icon_start, command = self.starte_lauf, bg = self.col_button_start, fg = self.text_buttons, font = self.settings.btn_font, compound="top", padx=10, width=bw)
        self.start_pause_btn.configure(state='disabled', background=self.col_button_end_disabled)
        self.start_pause_btn.grid(column = 0, row = lrow, padx = (0, 5), pady = (10, 0), sticky=tk.NW)

        self.stop_btn = tk.Button(left_panel, text = "Stop", command = self.stop, bg = self.col_button_end, fg = self.text_buttons, font = self.settings.btn_font, image=self.icon_stop, compound="top", padx = 10, width=bw)
        self.stop_btn.configure(state='disabled', background=self.col_button_end_disabled)
        self.stop_btn.grid(column = 0, row = lrow, padx = (0, 0), pady = (10,0), sticky=tk.NE)


        # ein Label, in dem man Läuferinfos anzeigen kann
        lrow += 1
        self.info_lbl = tk.Label(left_panel, text="Läuferinfos\n\n\n", bg=self.bg_dark, fg=self.color_text, font=self.settings.mid_font, anchor="w", justify="left", padx=10, pady=10, width=20)
        self.info_lbl.grid(column=0, row=lrow, sticky=tk.NE + tk.SW, padx=0, pady=20)
        self.info_lbl.config(borderwidth=2, relief="solid", bg=self.bg_light)


        # ======================================================================
        # rechts Panel mit den beiden Listen

        right_panel = tk.Frame(self, bg=self.bg_dark)
        right_panel.grid(column=1, row=0, sticky=tk.NE + tk.SW, padx=10, pady=10, rowspan=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Angekommen-Liste
        self.angekommen_lbl = tk.Label(right_panel, text=" Angekommen:", bg=self.bg_dark, fg=self.color_text, font=self.settings.mid_font, anchor="w")
        self.angekommen_lbl.grid(column=0, row=0, sticky=tk.NE + tk.SW, padx=0, pady=5)

        self.angekommen_lst = tk.Listbox(right_panel, bg=self.bg_dark, fg=self.color_text, font=self.settings.small_font)
        self.angekommen_lst.grid(column=0, row=1, sticky=tk.NE + tk.SW + tk.E + tk.W)
        angekommen_scrollbar = tk.Scrollbar(right_panel, orient=tk.VERTICAL)
        angekommen_scrollbar.grid(column=1, row=1, sticky=tk.NS)
        self.angekommen_lst.config(yscrollcommand=angekommen_scrollbar.set)
        angekommen_scrollbar.config(command=self.angekommen_lst.yview)

        # Button zum Sortieren der Einträge
        buttonpanel = tk.Frame(right_panel)

        self.nummer_sort_button = tk.Button(buttonpanel, text="ID", bg=self.color_info, fg=self.text_buttons, font=self.settings.small_font, command=lambda: self.sort_col(0))
        self.nummer_sort_button.grid(column=1, row=0)

        self.name_sort_button = tk.Button(buttonpanel, text="Na", bg=self.color_info, fg=self.text_buttons, font=self.settings.small_font, command=lambda: self.sort_col(2))
        self.name_sort_button.grid(column=2, row=0)

        self.angekommen_sort_button = tk.Button(buttonpanel, image=self.icon_sort, bg=self.color_info, fg=self.text_buttons, font=self.settings.small_font, command=lambda: self.sort_col(7))
        self.angekommen_sort_button.grid(column=3, row=0)

        buttonpanel.grid(column=0, columnspan=2, row=0, sticky=tk.NE)


        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)

        # Teilnehmer-Liste
        self.teilnehmer_lbl = tk.Label(right_panel, text=" Teilnehmer:", bg=self.bg_dark, fg=self.color_text, font=self.settings.mid_font, anchor="w")
        self.teilnehmer_lbl.grid(column=0, row=2, sticky=tk.NE + tk.SW, padx=0, pady=5)

        self.teilnehmer_lst = tk.Listbox(right_panel, bg=self.bg_dark, fg=self.color_text, font=self.settings.small_font)
        self.teilnehmer_lst.grid(column=0, row=3, sticky=tk.NE + tk.SW + tk.E + tk.W)

        tn_scrollbar = tk.Scrollbar(right_panel, orient=tk.VERTICAL)
        tn_scrollbar.grid(column=1, row=3, sticky=tk.NS)
        self.teilnehmer_lst.config(yscrollcommand=tn_scrollbar.set)
        tn_scrollbar.config(command=self.teilnehmer_lst.yview)

        self.angekommen_lst.bind("<<ListboxSelect>>", self.show_info_a)
        self.teilnehmer_lst.bind("<<ListboxSelect>>", self.show_info_t)

        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(3, weight=1)


    def sort_list(self):
        # Holen der Daten aus der Datenbank und Sortierung nach Zeit
        db = self.data.db
        runners = db.get_arrived_runners(self.run_id)
        runners_sorted = sorted(runners, key=lambda x: x[7])

        # Leeren der Listbox
        self.angekommen_lst.delete(0, tk.END)

        # Hinzufügen der sortierten Daten zur Listbox
        for runner in runners_sorted:
            tn_str = utils.format_teilnehmer_for_list(runner)
            self.angekommen_lst.insert(tk.END, tn_str)


    def sort_col(self, col):
        db = self.data.db
        runners = db.get_arrived_runners(self.run_id)
        if self.sort_ascending:
            runners.sort(key=lambda runner: runner[col])
        else:
            runners.sort(key=lambda runner: runner[col], reverse=True)
        self.angekommen_lst.delete(0, tk.END)
        for runner in runners:
            tn_str = utils.format_teilnehmer_for_list(runner)
            self.angekommen_lst.insert(tk.END, tn_str)
        self.sort_ascending = not self.sort_ascending


    def show_info_a(self, event):
        if self.angekommen_lst.curselection():
            selected_item = self.angekommen_lst.get(self.angekommen_lst.curselection())
            self.show_info_str(selected_item)


    def show_info_t(self, event):
        if self.teilnehmer_lst and self.teilnehmer_lst.curselection():
            selected_item = self.teilnehmer_lst.get(self.teilnehmer_lst.curselection())
            self.show_info_str(selected_item)


    def show_info_str(self, info_str):
        id = info_str.split(",")[0].strip()
        d = self.data
        # tn = d.find_teilnehmer(d.get_alle_teilnehmer(), id)
        tn = d.find_teilnehmer(id)
        tn_str = utils.format_teilnehmer_for_info(tn)
        self.info_lbl.config(text=tn_str)


    def activate_ui(self):
        self.start_pause_btn.configure(state='normal')
        text = self.start_pause_btn.cget("text")
        if text == "reset":
            self.start_pause_btn.configure(background=self.color_info)
        else:
            self.start_pause_btn.configure(background=self.color_running)


    # =========================================================================
    # === Listen

    def add_teilnehmer(self, tn):
        entry = tn[1] + " " + tn[2]
        self.teilnehmer_lst.insert(-1, entry)
        self.count_teilnehmer()


    def reset_lists(self):
        # print("\nreset lists " + self.run_id)
        self.teilnehmer_lst.delete(0, tk.END)
        self.angekommen_lst.delete(0, tk.END)

        r = self.data.db.get_runners()

        active_runners = self.data.db.get_not_arrived_runners(self.run_id)
        if not self.data.db.run_has_runners(self.run_id):
            # print("keine Läufer vorhanden -> Stop run")
            self.stop_run()


        # Aktive Läufer setzen
        if self.data.db.run_is_finished(self.run_id):
            # print("Lauf ist schon beendet -> active_runners leeren")
            active_runners = []
            # active_runners = self.data.db.get_not_arrived_runners(self.run_id)

        if len(active_runners) == 0:
            active_runners = self.data.db.get_all_runners_from_run(self.run_id)
            # print(f"Es gibt insgesamt {len(active_runners)} Läufer")
        else:
            active_runners = self.data.db.get_not_arrived_runners(self.run_id)
            # print(f"Es sind noch {len(active_runners)} Läufer unterwegs")


        for runner in active_runners:
            entry = utils.format_teilnehmer_for_list(runner)
            self.teilnehmer_lst.insert(tk.END, entry)

        # Angekommene Läufer setzen
        arrived_runners = self.data.db.get_arrived_runners(self.run_id)
        # print(f"Es sind {len(arrived_runners)} Läufer angekommen")
        for runner in arrived_runners:
            entry = utils.format_teilnehmer_for_list(runner)
            self.angekommen_lst.insert(tk.END, entry)


        # print("aktive Läufer:")
        na = self.data.db.get_not_arrived_runners(self.run_id)
        # print(f"es sind {len(na)} Läufer unterwegs")
        if len(na) == 0 and self.data.db.run_is_finished(self.run_id):
            self.teilnehmer_lst.delete(0, tk.END)


        if not self.data.db.run_is_active(self.run_id):
            # print("Lauf ist nicht aktiv")
            self.activate_ui()

        self.count_teilnehmer()



    def count_teilnehmer(self):
        tn = "Läufer: " + str(self.teilnehmer_lst.size())
        self.teilnehmer_lbl.config(text=tn)
        angekommen = "Angekommen: " + str(self.angekommen_lst.size())
        self.angekommen_lbl.config(text=angekommen)



    def starte_lauf(self):
        timestamp = self.data.starte_lauf(self.run_id)
        self.start_time = timestamp
        self.seconds = 0
        self.start_timer(timestamp)
        time_str = time.strftime(self.data.timeformat)
        self.startzeit_lbl.config(text = time_str)
        self.parent.start_run(self.run_id, timestamp)

        # Layout-Gedöns
        # self.title_lbl.config(bg=green)
        self.config(highlightbackground=self.color_running)
        if self.data.settings.style == self.data.settings.STYLE_COLORFUL:
            self.startzeit_lbl.config(fg = self.color_running)
            self.aktuelle_zeit_lbl.config(fg = self.color_running)
            self.teilnehmer_lst.config(fg = self.color_running)
        self.start_pause_btn.config(background=self.color_running_light, state = "disabled")
        self.stop_btn.configure(background=self.color_inactive, state='normal')

        self.update_timer()


    def resume_run(self, timestamp):
        self.seconds = 0
        self.start_timer(timestamp)
        time_str = timestamp.strftime(self.parent.data.timeformat)

        self.parent.start_run(self.run_id, timestamp)
        self.startzeit_lbl.config(text = time_str)

        # self.title_lbl.config(bg=green)
        self.config(highlightbackground=self.color_running)

        if self.data.settings.style == self.data.settings.STYLE_COLORFUL:
            self.startzeit_lbl.config(fg = self.color_running)
            self.aktuelle_zeit_lbl.config(fg = self.color_running)
            self.teilnehmer_lst.config(fg = self.color_running)
        self.start_pause_btn.config(background=self.color_running_light, state = "disabled")
        self.stop_btn.configure(background=self.color_inactive, state='normal')
        self.update_timer()


    def load_finished_run(self, start, end):
        # print("loading finished run")
        self.stop_run(end)
        # self.stop_run()

    """
    def set_run_times(self, start, end):
        '''
        self.set_endtime(end)
        self.stop_btn.configure(background=red, state='disabled')
        self.teilnehmer_lst.config(fg = white)
        '''
        self.is_running = False
        self.stop_btn.config(background=red_light, state = "disabled")
        # Der start-Button wird jetzt zum Reset-Button. So kann man einen Lauf nochmal ganz neu starten.
        self.start_pause_btn.config(bg=blue, state = "normal", text="reset", command=self.reset_run)

        self.startzeit_lbl.config(text = start)
        self.aktuelle_lbl.config(text="Beendet um ")
        # str_time = end.strftime(self.parent.data.timeformat)
        self.aktuelle_zeit_lbl.config(text=end)
    """


    # =========================================================================
    # === timer
    # =========================================================================

    def update_timer(self):
        self.parent.update()
        if self.is_running:
            # print("starttine:")
            # print(self.start_time)
            self.elapsed_time = datetime.now() - self.start_time
            time_str = utils.timedelta_formatter(self.elapsed_time)[:-1]
            if time_str != None:
                self.aktuelle_zeit_lbl.configure(text=time_str)
                self.after(100, self.update_timer)
        else:
            self.elapsed_time = 0


    def start_timer(self, timestamp):
        self.start_time = timestamp
        self.is_running = True

    # =========================================================================

    def stop(self):
        if self.teilnehmer_lst.size() > 0:
            if messagebox.askyesno("Lauf beenden", "Soll der Lauf wirklich beendet werden?\nEs sind noch Läufer unterwegs!"):
                self.stop_run()
        elif messagebox.askyesno("Lauf beenden", "Soll der Lauf wirklich beendet werden?"):
                self.stop_run()



    def stop_run(self, endtime=None):
        # print("stopping run")

        self.is_running = False
        self.stop_btn.config(background=self.color_inactive_light, state = "disabled")
        # Der start-Button wird jetzt zum Reset-Button. So kann man einen Lauf nochmal ganz neu starten.
        self.start_pause_btn.config(bg=self.color_info, state = "normal", text="reset", command=self.reset_run)
        self.config(highlightbackground=self.color_finished)
        if self.data.settings.style == self.data.settings.STYLE_COLORFUL:
            self.startzeit_lbl.config(fg = self.color_finished)
            self.aktuelle_zeit_lbl.config(fg = self.color_finished)
            self.teilnehmer_lst.config(fg=self.color_text)
            self.angekommen_lst.config(fg=self.color_finished)
        if not endtime or endtime == None:
            # print("regular stop")
            timestamp = self.data.stop_run(self.run_id)
            str_time = timestamp.strftime(self.data.timeformat)
            self.aktuelle_lbl.config(text="Beendet um ")
            self.parent.mark_finished_run(self.run_id)
        else:
            # print("gestoppter lauf geladen")
            # self.set_endtime(str_time)
            self.data.stop_run(self.run_id)
            str_time = endtime.strftime(self.data.timeformat)
            self.aktuelle_lbl.config(text="Beendet um ")
            self.aktuelle_zeit_lbl.config(text=str_time)
            # Anzeige in der linken Leiste noch anpassen:
            self.parent.mark_finished_run(self.run_id)


    def reset_run(self):
        # start und ende auf 0 setzen
        # alle läufer des Laufs suchen und deren Zeit auf 0 setzen
        self.data.reset_run(self.run_id)
        # alle läufer aus lst_angekommen entfernen und in lst_teilnehmer setzen
        self.reset_lists()
        # angezeigte Zeit und Startbutton resetten
        self.config(highlightbackground=self.color_info)
        if self.data.settings.style == self.data.settings.STYLE_COLORFUL:
            self.startzeit_lbl.config(text="00:00:00", fg = self.color_info)
            self.aktuelle_lbl.config(text="Laufzeit: ")
            self.aktuelle_zeit_lbl.config(text="00:00:00.00", fg = self.color_info)
        self.start_pause_btn.configure(text = "Lauf starten", command = self.starte_lauf, bg = self.col_button_start)
        self.parent.reset_run(self.run_id)


    def set_endtime(self, str_time):
        self.aktuelle_lbl.config(text="Beendet um ")
        self.aktuelle_zeit_lbl.config(text=str_time)
        self.parent.finish_run(self.run_id, str_time)
        self.data.stop_run(self.run_id)
        # self.set_endtime(str_time)


    def get_elapsed_time(self):
        # elapsed_time = datetime.datetime.now() - self.start_time
        elapsed_time = datetime.now() - self.start_time
        return elapsed_time


    def create_runnerinfo(tn):
        str = tn['vorname'] + " " + tn['nachname'] + "\n"
        str += "ID: " + tn['id'] + "\n"
        str += "Geburtsjahr: " + tn['jahr']
        if self.data.is_running(tn):
            str += "läuft noch"
        else:
            str += tn['zeit']
        return str
