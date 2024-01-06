from datetime import datetime, time

from service_functions import *
from classes import *
import locale

def parse_infos(soup):
    # Setze das Locale auf Deutsch
    locale.setlocale(locale.LC_TIME, 'de_DE')
    
    history_items = soup.find("div", {"data-automation-id": "activity-history-items"})
    items = history_items.find_all("li")


    date = None
    serie_staffel = None
    serie = None
    staffel = None
    special_o_movie = None
    folgennummer = None
    Serien = {}

    for item in items:
        # Datum extrahieren
        # Extracting the date
        found_date = False
        folgennummer = None
        folgentitel = None

        try:
            date_element = item.find("div", {"class": "RdNoU_"})
            date = date_element.text.strip()
            found_date = True
        except:
            found_date = False

        if not found_date:
            found_series = False
            try:
                title_element = item.find("div", {"class": "k4n17D"})
                serie_staffel = title_element.text.strip()
                found_series = True
            except:
                found_series = False

            try:
                serie, staffel = extract_ser_sn(serie_staffel)
            except:
                special_o_movie = True

            if not found_series:
                try:
                    episode_element = item.find("div", {"class": "S6ogEA"})
                    folgenummer_tag = episode_element.p.text.strip()
                    # folgenummer_tag = item.find('p')
                except:
                    folgenummer_tag = None
                    # pass

                if folgenummer_tag:
                    folgennummer, folgentitel = extract_epsn_en(folgenummer_tag)

                    # Konvertiere den String in ein datetime-Objekt
                    datum_obj = datetime.strptime(date, "%d. %B %Y")
                    # Setze die Uhrzeit auf 12:00 Uhr mittags
                    datum_mittags = datetime.combine(datum_obj.date(), time(12, 0))

                    if not serie in Serien:
                        Serien[serie] = Serie(serie)

                    Serien[serie].add_staffel(staffel)
                    Serien[serie].staffeln[staffel].add_episode(nummer=folgennummer, titel=folgentitel, datum=datum_mittags)

                    # print(
                    #     f"Datum: {datum_mittags} | Serie: {serie} | Staffel: {staffel} | Folgennummer: {folgennummer} | Folgentitel: {folgentitel}"
                    # )
    return Serien