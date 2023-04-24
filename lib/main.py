import os
import tkinter as tk

from gui import MainWindow
from model import Data
from model.settings import Settings


data = None

def main():
    root = tk.Tk()
    settings = Settings()

    data = Data(settings)
    data.read_data()
    app = MainWindow(root, data)
    app.pack()


    def save_data_periodically():
        # nur speichern, solange noch ein Lauf aktuv ist.
        is_running = data.db.waldlauf_active()
        if is_running:
            data.write_data()
            root.after(settings.AUTOSAVE, save_data_periodically)


    def on_closing():
        app.quit()


    # rufe on_closing() auf, wenn das Fenster geschlossen wird
    root.after(settings.AUTOSAVE, save_data_periodically)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
