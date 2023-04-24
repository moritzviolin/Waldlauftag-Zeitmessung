class Timepicker(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("TimePicker Dialog")

        # TimePicker-Widget hinzufügen
        self.time_picker = ttk.TimePicker(self, orient='vertical', padding=10)
        self.time_picker.pack(pady=10)

        # OK-Button hinzufügen, um die ausgewählte Uhrzeit zu bestätigen und den Dialog zu schließen
        ok_button = ttk.Button(self, text="OK", command=self.on_ok_clicked)
        ok_button.pack(pady=10)

    def on_ok_clicked(self):
        selected_time = self.time_picker.get()
        print("Selected time:", selected_time)

        self.destroy()
