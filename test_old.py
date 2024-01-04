from bs4 import BeautifulSoup
import re
import json
import os
import sys

from classes import *
from credentials import *
from autologin import crawl_amazon

page = "https://www.amazon.com/gp/video/settings/watch-history"

# Pfad zum aktuellen Skript
script_path = os.path.abspath(sys.argv[0])
sel_timeout = 60


soup = crawl_amazon(page=page, username=username, password=password, otp=totp)


# with open('wholepage.html', 'r', encoding='utf-8') as file:
#     html_code = file.read()

# # Parse the HTML code
# soup = BeautifulSoup(html_code, 'html.parser')

# items = html_code
# Extrahiere Informationen
history_items = soup.find("div", {"data-automation-id": "activity-history-items"})
items = history_items.find_all("li")
# print(type(items))


date = None
serie_staffel = None
serie = None
staffel = None
special_o_movie = None
folgennummer = None


for item in items:
    # Extrahiere Datum, Serie, Staffel, Folgennummer und Folgentitel
    # date = item.find('div', {'data-automation-id': re.compile(r'wh-date-.*')}).div.text.strip()
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

        if "-" in serie_staffel:
            try:
                serie = serie_staffel.split("-")[0].strip()
                staffel = serie_staffel.split("-")[-1].strip()
            except:
                special_o_movie = True

        elif "–" in serie_staffel:
            try:
                serie = serie_staffel.split("–")[0].strip()
                staffel = serie_staffel.split("–")[-1].strip()
            except:
                special_o_movie = True

        else:
            try:
                serie = serie_staffel.split("–")[0].strip()
                staffel = serie_staffel.split("–")[-1].strip()
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
                # String bei ':' splitten
                # splitted_string = episode_string.split(':')

                # # Ergebnis ausgeben
                # print(f'Teil 1: {splitted_string[0].strip()}')
                # print(f'Teil 2: {splitted_string[1].strip()}')
                folgennummer = folgenummer_tag.split(":")[
                    0
                ].strip()  # if folgenummer_tag else None
                folgentitel = folgenummer_tag.split(":")[
                    1
                ].strip()  # if folgenummer_tag else None

                print(
                    f"Datum: {date} | Serie: {serie} | Staffel: {staffel} | Folgennummer: {folgennummer} | Folgentitel: {folgentitel}"
                )
        # print("Serie:", serie)
        # print("Staffel:", staffel)
        # print("Folgennummer:", folgennummer)
        # print("Folgentitel:", folgentitel)

    # try:
    #     date = item["date"]
    # except KeyError:
    #     date = None

    # try:
    #     title_data = item["titles"][0]["title"]["text"]
    #     match = re.match(r"Folge (\d+): (.+)", title_data)
    #     folgennummer, folgentitel = match.group(1, 2)
    # except (KeyError, IndexError, AttributeError):
    #     folgennummer, folgentitel = None, None

    # try:
    #     serie = item["titles"][0]["title"]["text"].split(" - ")[0]
    # except (KeyError, IndexError, AttributeError):
    #     serie = None

    # print("Datum:", date)
    # print("Serientitel:", serie)
    # print("Folgennummer:", folgennummer)
    # print("Folgentitel:", folgentitel)
