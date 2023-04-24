╔════════════╗
║ Datenbasis ║
╚════════════╝

Die csv-Datei mit den Läufern muss im Verzeichnis data/ liegen und "daten.csv" heißen. Diese Datei darf nur die Daten enthalten, KEINE Überschriften. Wenn die Werte nicht nurch ein , getrennt sind, muss die config.ini angepasst werden.
Wichtig: Jede ID muss eine eindeutige Zahl sein! Buchstaben sind nicht erlaubt. 
Wenn ein Läufer bei mehreren Läufen mitläuft, braucht er für jeden Lauf eine eigene, eindeutige ID!
Eine Beispiel-Datei liegt unter docs/

Die Spalten der daten.csv Datei sollen wie folgt gefüllt sein:

| ID | Vorname | Nachname | Geschlecht | Klasse | Jahrgang | Lauf |

Die Spalte Klasse kann auch zur Kennzeichnung von Lehrern und Ehemaligen genutzt werden. 
Die Laufbezeichnungen sind wie folgt:

3   -> 3 km Lauf
5_1 -> 1. 5 km Lauf
5_2 -> 2. 5 km Lauf
10  -> 10 km Lauf


╔════════════╗
║  Starten   ║
╚════════════╝

Das Programm wird durch einen Doppelklick auf "zeitmessung.bat" gestartet.
Einstellungen können in config.ini  angepasst werden.
Dort gibt es zwei Farb-Versionen, eine helle und eine dunkle. 


╔════════════╗
║ Ergebnisse ║
╚════════════╝

Die Ergebnisse werden im Verzeichnis ergebnisse/ gespeichert.
Es kann sein, dass dort mehrere Dateien zum selben Lauf liegen. Das kann daran liegen, dass ein Lauf erneut gestartet wurde. Wenn ein Lauf zwischendurch neu gestartet wurde, wird das im Logfile vermerkt.
Die Uhrzeit im Dateinamen gibt immer die Startzeit des Laufs an.




══════════════════════════════════════════════════════════════════════════════════════════

Getestet mit python 3.10.7 und 3.10.10
