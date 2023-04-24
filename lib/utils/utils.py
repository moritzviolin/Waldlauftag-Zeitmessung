def make_time_str(time: float):
    # Formatiert die Zeit in ein menschenlesbares Format
    time += 7200 # +7200(sekunden) als Zeitzonenausgleich zwischen CEST und UTC
    hundertstel = int((time % 1) * 100)
    sekunden = int(time % 60)
    minuten = int(((time % 86400) % 3600) // 60)
    stunden = int((time % 86400) // 3600)
    return (str(stunden).rjust(2, '0') + ":" + str(minuten).rjust(2, '0') + ":" + str(sekunden).rjust(2, '0') + "." + str(hundertstel).rjust(2, '0'))



def timedelta_formatter(td):                             # defining the function
    td_sec = td.seconds                                  # getting the seconds field of the timedelta
    hour_count, rem = divmod(td_sec, 3600)               # calculating the total hours
    minute_count, second_count = divmod(rem, 60)         # distributing the remainders
    milliseconds = td.microseconds // 1000                             # extracting milliseconds field
    str = "{:0>2d}:{:0>2d}:{:0>2d}.{:0>3d}".format(hour_count,minute_count,second_count,milliseconds)
    return str


def format_teilnehmer_for_list(tn):
    entry = str(tn[0]) + ", " + tn[2] + ", " + tn[1] # + " (" + tn[4] + ")"
    zeit = tn[7]
    if zeit != None and len(str(zeit)) > 1:
        entry += " ( " + zeit + " )"
    return entry


def format_teilnehmer_for_info(tn):
    s = "Läuferinfos:\n"
    s += tn[1] + " " + tn[2] + " (" + tn[4] + ")\n"
    # s += "Läufernummer:\t"+ tn[0] + "\n"
    s += "Jahrgang: \t" + str(tn[5]) + "\n"
    zeit = tn[7]
    if zeit and len(str(zeit)) > 1:
        s += "Laufzeit:   \t" + str(zeit)
    return s
