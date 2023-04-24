import configparser
import os
# import os.path.join as join



class Settings:
    # die IDs in der csv-Datai
    RUN_3 = "3"
    RUN_5_1 = "5_1"
    RUN_5_2 = "5_2"
    RUN_10 = "10"

    # der angezeigte Name in der Oberfläche
    RUN_3_NAME = "3-km-Lauf"
    RUN_5_1_NAME = "5-km-Lauf #1"
    RUN_5_2_NAME = "5-km-Lauf #2"
    RUN_10_NAME = "10-km-Lauf"

    STYLE_COLORFUL = "colorful"
    STYLE_SIMPLE = "simple"


    bg_light = "#333548"        # helleres grau
    bg_dark = "#1A1B25"         # dunkleres grau
    color_text = "#F9F9F9"      # off-white
    text_buttons = "#1A1B25"
    bg_input = "#08090C"        # fast-schwarz. Wichtig: Kontrastfarbe zur Schrift !

    # Farbe, um alles anzuzeigen, was mit einem aktiven Lauf zu tun hat
    # Startbutton, aktive Läufer, Schrift
    color_running = "#93c446"   # grün
    color_running_light = "#D8FDE5"

    # Farbe, um alles anzuzeigen, was mit einem beendeten Lauf zu tun hat
    # angekommene Läufer in Liste, Text "beendet" in Seitenleiste
    color_finished = "#FFCB2E"  # orange

    # Stop-Button, Programm beenden
    color_inactive = "#C1322B"  # rot
    color_inactive_light = "#F6CAD3"

    # Farbe für 'Daten speichern'-  und Reset-Button
    color_info = "#87A6F0"      # blau
    color_info_light = "#ADE7FF"


    # nach dieser Zeit wird automatisch gespeichet (Millisekunden! 60000 = eine Minute
    AUTOSAVE = 60000

    # Infodatei mit Start- und Endzeit von jedem lauf
    INFOFILE = "ergebnisse/info.csv"

    # CSV-Datei mit den Teilnehmern
    DATAFILE = "data/daten.csv"

    # Separator für csv
    SEP = ","

    # Texte
    MSG_TN_NICHT_GESTARTET = "Teilnehmer ist noch nicht gestartet"
    MSG_TN_UNBEKANNT = "Teilnehmer unbekannt"
    MSG_TN_SCHON_ANGEKOMMEN = "Teilnehmer schon im Ziel"

    # intern
    large_font = None
    mid_font = None
    small_font = None
    btn_font = None

    def __init__(self):
        # Erstellen Sie ein Konfigurationsparser-Objekt
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        config = configparser.ConfigParser()
        # Laden Sie die INI-Datei
        filename = os.path.join(self.base_dir, "config.ini")
        result = config.read(filename)

        if result:
            print(f"Die config-Datei {filename} wurde gefunden und erfolgreich gelesen.")
            self.AUTOSAVE = config.getint('main', 'autosave')
            self.INFOFILE = config.get('main', 'infofile')
            self.DATAFILE = config.get('main', 'datafile')
            self.SEP = config.get('main', 'sep')
            self.style = config.get('main', 'style')
            # self.darkmode = config.get('main', 'darkmode') == "true"

            self.farbschema = self.style = config.get('main', 'farbschema').strip('"')

            # Farben
            self.bg_light = config.get(self.farbschema, 'bg_light').strip('"')
            self.bg_dark = config.get(self.farbschema, 'bg_dark').strip('"')
            self.color_text = config.get(self.farbschema, 'color_text').strip('"')
            self.text_buttons = config.get(self.farbschema, 'text_buttons').strip('"')
            self.bg_input = config.get(self.farbschema, 'bg_input').strip('"')
            self.color_running = config.get(self.farbschema, 'color_running').strip('"')
            self.color_running_light = config.get(self.farbschema, 'color_running_light').strip('"')
            self.color_finished = config.get(self.farbschema, 'color_finished').strip('"')
            self.color_inactive = config.get(self.farbschema, 'color_inactive').strip('"')
            self.color_inactive_light = config.get(self.farbschema, 'color_inactive_light').strip('"')
            self.color_info = config.get(self.farbschema, 'color_info').strip('"')
            self.color_info_light = config.get(self.farbschema, 'color_info_light').strip('"')

            '''
            print("Folgende Werte wurden eingelesen: ")
            for section in config.sections():
                print(f"[{section}]")
                for key, value in config.items(section):
                    print(f"{key} = {value}")
            '''
        else:
            print(f"Die Datei {filename} konnte nicht gelesen werden. Es werden Standardwerte verwendet.")
