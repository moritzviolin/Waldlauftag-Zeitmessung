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
import model.settings

from gui.runpanel import RunPanel

from model import settings
from utils import utils


# ============================================================================
# === Dialog: Weiterer Teilnehmer
# ============================================================================

class AddParticipantDialog(tk.Toplevel):
    # def __init__(self, parent, is_running_run_3, is_running_run_5_1, is_running_run_5_2, is_running_run_10):
    def __init__(self, parent, data):
        super().__init__(parent)

        self.title("Teilnehmer hinzufügen")
        self.geometry("600x650") # Breite x Höhe
        self.resizable(False, False)
        self.result = None
        self.parent = parent
        self.data = data
        self.settings = data.settings

        self.col_button_start = self.settings.color_running
        self.col_button_start_disabled = self.settings.color_running_light
        self.col_button_end = self.settings.color_inactive
        self.col_button_end_disabled = self.settings.color_inactive_light
        self.col_button_data = self.settings.color_info
        self.color_info = self.settings.color_info
        self.bg_dark = self.settings.bg_dark
        self.bg_light = self.settings.bg_light
        self.color_text = self.settings.color_text
        self.color_running = self.settings.color_running


        # Center dialog on parent window
        self.withdraw()
        self.update_idletasks()
        self.configure(bg=self.bg_light)
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry("+{}+{}".format(x, y))
        self.deiconify()


        style = ttk.Style()
        style.configure("TRadiobutton", background=self.bg_light, foreground=self.color_text, font=data.settings.mid_font)
        style.configure("TButton", fg = self.bg_dark, font = data.settings.btn_font)

        header_label = tk.Label(self, text="Neuer Teilnehmer", font=data.settings.large_font, fg=self.color_text, bg=self.bg_light)
        header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Labels and input fields
        self.labels = ["ID:", "Vorname:", "Nachname:", "Klasse:", "Geschlecht:", "Geburtsjahr:", "Lauf:"]
        self.inputs = {}
        self.infolabel = tk.Label(self, background=self.bg_light, foreground=self.settings.color_inactive, font=data.settings.large_font)
        i = 0
        for i, label in enumerate(self.labels):
            i += 1
            tk.Label(self, text=label, background=self.bg_light, foreground=self.color_text, font=data.settings.mid_font).grid(row=i, column=0, padx=10, pady=10, sticky="nw")
            if label == "Geschlecht:":
                self.gender_var = tk.StringVar(value="")
                gender_frame = tk.Frame(self, bg=self.bg_light)
                gender_frame.grid(row=i, column=1, padx=10, pady=10, sticky="nw")

                gender_m = ttk.Radiobutton(gender_frame, text="männlich", variable=self.gender_var, value="m", style="TRadiobutton")
                gender_m.grid(row=0, column=0, padx=20, pady=5, sticky="w")

                gender_w = ttk.Radiobutton(gender_frame, text="weiblich", variable=self.gender_var, value="w", style="TRadiobutton")
                gender_w.grid(row=1, column=0, padx=20, pady=5, sticky="w")

                gender_d = ttk.Radiobutton(gender_frame, text="divers", variable=self.gender_var, value="d", style="TRadiobutton")
                gender_d.grid(row=2, column=0, padx=20, pady=5, sticky="w")

            elif label == "Lauf:":
                # self.inputs[label] = ttk.Combobox(self, values=["3km-Lauf", "1.5km-Lauf", "10km-Lauf", "2. 5km-Lauf"])
                self.lauf_var = tk.StringVar(self)
                self.lauf_var.set("3km-Lauf")

                lauf_frame = tk.LabelFrame(self, fg=self.color_text, bg=self.bg_light, font=data.settings.mid_font)
                lauf_frame.grid(row=i, column=1, padx=10, pady=10, sticky="w", columnspan=2)
                lauf_frame.config(width=400, borderwidth=0, highlightthickness=0, bg=self.bg_light)

                three_km_button = ttk.Radiobutton(lauf_frame, text=data.settings.RUN_3_NAME, variable=self.lauf_var, value=data.settings.RUN_3, style="TRadiobutton")
                three_km_button.grid(row=0, column=0, padx=20, pady=5, sticky="w")
                if self.parent.data.run_is_active(data.settings.RUN_3) or self.parent.data.run_is_finished(data.settings.RUN_3):
                    three_km_button.config(state="disabled")

                one_five_km_button = ttk.Radiobutton(lauf_frame, text=data.settings.RUN_5_1_NAME, variable=self.lauf_var, value=data.settings.RUN_5_1)
                one_five_km_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")
                if self.parent.data.run_is_active(data.settings.RUN_5_1) or self.parent.data.run_is_finished(data.settings.RUN_5_1):
                    one_five_km_button.config(state="disabled")

                ten_km_button = ttk.Radiobutton(lauf_frame, text=data.settings.RUN_10_NAME, variable=self.lauf_var, value=data.settings.RUN_10)
                ten_km_button.grid(row=1, column=0, padx=20, pady=5, sticky="w")
                if self.parent.data.run_is_active(data.settings.RUN_10) or self.parent.data.run_is_finished(data.settings.RUN_10):
                    ten_km_button.config(state="disabled")

                second_five_km_button = ttk.Radiobutton(lauf_frame, text=data.settings.RUN_5_2_NAME, variable=self.lauf_var, value=data.settings.RUN_5_2)
                second_five_km_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")
                if self.parent.data.run_is_active(data.settings.RUN_5_2) or self.parent.data.run_is_finished(data.settings.RUN_5_2):
                    second_five_km_button.config(state="disabled")
            elif label == "ID:":
                self.inputs[label] = ttk.Entry(self, width=35)
                self.inputs[label].grid(row=i, column=1, padx=10, pady=10)
                new_id = self.data.db.get_next_free_id()
                # self.inputs[label].config(value=str(new_id))
                self.inputs[label].insert(0, str(new_id))
            elif label == "Vorname:":
                self.inputs[label] = ttk.Entry(self, width=35)
                self.inputs[label].grid(row=i, column=1, padx=10, pady=10)
                self.inputs[label].focus()
            else:
                self.inputs[label] = ttk.Entry(self, width=35)
                self.inputs[label].grid(row=i, column=1, padx=10, pady=10)
        i+=1
        self.infolabel.grid(row=i, column=0, columnspan=2, padx=10, pady=10, sticky="nw")


        # Buttons
        mybutton = ttk.Button(self,text="Abbrechen", command=self.destroy)
        mybutton.config(style="TButton")
        mybutton.grid(row=len(self.labels)+2, column=0, padx=10, pady=10, sticky="e")
        ttk.Button(self, text="Hinzufügen", command=self.ok_clicked).grid(row=len(self.labels)+2, column=1, padx=10, pady=10, sticky="e")


    def ok_clicked(self):
        # Get the values of all the input fields
        id = self.inputs["ID:"].get()
        vorname = self.inputs["Vorname:"].get()
        nachname = self.inputs["Nachname:"].get()
        # geschlecht = self.inputs["Geschlecht:"].get()
        klasse = self.inputs["Klasse:"].get()
        geschlecht = self.gender_var.get()
        jahrgang = self.inputs["Geburtsjahr:"].get()
        lauf = self.lauf_var.get()
        # Create a dictionary with the input values and set the result attribute
        # Hier sollte man noch prüfen, ob Geschlecht und Lauf ausgewählt wurden.
        # Falls nicht, Hinweis geben.
        if id.strip() != "" and vorname.strip() != "" and nachname.strip() != "" and geschlecht.strip() != "" and klasse.strip() != "" and jahrgang.strip() != "" and lauf.strip() != "":
            self.result = {"id": id, "vorname": vorname, "nachname": nachname, "geschlecht": geschlecht, "klasse":klasse, "jahrgang": jahrgang, "lauf": lauf, "zeit": 0}
            # Close the dialog window
            self.destroy()
        else:
            self.infolabel.config(text="Bitte alle Felder ausfüllen!")


    def cancel_clicked(self):
        # Set the result attribute to None and close the dialog window
        self.result = None
        self.destroy()
