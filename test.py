from bs4 import BeautifulSoup
import re
import json
from classes import *

# with open('wholepage.html', 'r', encoding='utf-8') as file:
#     html_code = file.read()
# with open('output1.html', 'r', encoding='latin-1') as file:
with open('wholepage.html', 'r', encoding='utf-8') as file:
    html_code = file.read()

# Parse the HTML code
soup = BeautifulSoup(html_code, 'html.parser')
# items = html_code
# Extrahiere Informationen
# history_items = soup.find('div', {'data-automation-id': 'activity-history-items'})
# items = history_items.find_all('li')
# print(type(items))
# Checkboxen innerhalb des gewünschten div-Elements finden
# watch_history_div = soup.find('div', {'data-automation-id': 'watch-history'})
# checkboxes = watch_history_div.find_all('input', {'type': 'checkbox'})

# Checkboxen auflisten
# for checkbox in checkboxes:
#     print(checkbox)

# # Find all checkboxes
# checkboxes = soup.find_all('input', {'type': 'checkbox'})

# Extract information about each checkbox
# for checkbox in checkboxes:
#     checkbox_id = checkbox.get('id')
#     label = soup.find('label', {'for': checkbox_id}).text
#     print(f"Checkbox ID: {checkbox_id}, Label: {label}")
# print(items)
# for item in items:
    # Extrahiere Datum, Serie, Staffel, Folgennummer und Folgentitel
    # date = item.find('div', {'data-automation-id': re.compile(r'wh-date-.*')}).div.text.strip()
    # Datum extrahieren
    # try:
    #     date_tag = item.find('div', {'data-automation-id': re.compile(r'wh-date-.*')})
    #     date = date_tag.div.text.strip() if date_tag else None
    # except:
    #     date = None

    # try:
    #     serie_tag = item.find('a', {'class': '_1NNx6V Nwyhwn'})
    #     serie = serie_tag.text.strip() if serie_tag else None
    # except:
    #     serie = None

    # try:
    #     staffel = serie.split('–')[-1].strip() if serie else None
    # except:
    #     staffel = None

    # try:
    #     folgenummer_tag = item.find('p')
    #     folgennummer = folgenummer_tag.text.split(':')[0].strip() if folgenummer_tag else None
    # except:
    #     folgennummer = None

    # try:
    #     folgentitel = folgenummer_tag.text.split(':')[1].strip() if folgenummer_tag else None
    # except:
    #     folgentitel = None

    # # if date and serie and staffel and folgennummer and folgentitel:
    # if date:
    #     # Ausgabe der extrahierten Daten
    #     print("Datum:", date)
    #     print("Serie:", serie)
    #     print("Staffel:", staffel)
    #     print("Folgennummer:", folgennummer)
    #     print("Folgentitel:", folgentitel)
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

def extract_ser_sn(name):
    # Definiere das Muster für den Serientitel und die Staffelnummer
    muster = [re.compile(r'(.+) – Staffel (\d+)'), re.compile(r'(.+) - Staffel (\d+)')]

    for mus in muster:
        # Suche nach Übereinstimmungen im Namen
        ergebnis = mus.match(name)
        if ergebnis:
            break

    serientitel, staffelnummer = None, None
    if ergebnis:
        serientitel = ergebnis.group(1)
        staffelnummer = ergebnis.group(2)
        # print(f"Seriennamen: {serientitel}")
        # print(f"Staffelnummer: {staffelnummer}")
    elif "special" in name.lower():
        serientitel = name
        staffelnummer = "Special"
    else:
        print(f"Kein Seriennamen gefunden: {name}")

    return serientitel, staffelnummer

def extract_epsn_en(name):
    # Definiere das Muster für die Folgennummer und den Folgentitel
    muster = re.compile(r'Folge (\d+): (.+)')

    # Suche nach Übereinstimmungen im Folgennamen
    ergebnis = muster.match(name)

    folgennummer, folgentitel = None, None
    if ergebnis:
        folgennummer = ergebnis.group(1).zfill(2)  # Fülle mit Nullen auf, um sicherzustellen, dass die Nummer zwei Stellen hat
        folgentitel = ergebnis.group(2)
        # print(f"Folgennummer: {folgennummer}")
        # print(f"Folgentitel: {folgentitel}")
    else:
        print(f"Keine Nummer gefunden: {name}")

    return folgennummer, folgentitel

Serien = {}
for script_tag in soup.find_all('script', {'type': 'text/template'}):
    if '{"props":{"metadata":{"availability"' in script_tag.text:
        # Verarbeiten Sie diesen Tag weiter
        # Laden Sie die JSON-Daten
        json_data = json.loads(script_tag.text)
        for cont in json_data["props"]["widgets"]:
            if "ActivityHistoryOutput" in cont["content"]["__type"]:
                # print(cont["content"]["titles"])
                # print(cont["content"]["strings"])
                # print(type(cont["content"]))
                titles = cont["content"]["content"]["titles"]
                for tit in titles:
                    date = tit["date"]
                    # print(type(tit["titles"]))
                    for ele in tit["titles"]:
                        serientitle = ele["title"]["text"]
                        for types in ele["children"]:
                            folgentitel = types["title"]["text"]
                            # print(types["title"]["text"])
                            print(f"Datum: {date}")
                            serie, staffel = extract_ser_sn(serientitle)
                            folgennummer, folgentitel_n = extract_epsn_en(folgentitel)
                            
                            # ser_namen = [ x.name for x in Serien]

                            # if not serie in ser_namen:
                            #     Serien.append(Serie(serie))
                            #     # print(serie)
                            if serie:
                                if not serie in Serien:
                                    Serien[serie] = Serie(serie)

                                Serien[serie].add_staffel(staffel)
                                Serien[serie].staffeln[staffel].add_episode(nummer=folgennummer, titel=folgentitel_n, datum=date)

print(Serien)
# for _serie in Serien:
#    print(_serie.name)
                            # print(f"Serie: {serie}")
                            # print(f"Staffel: {staffel}")
                            # print(f"Folgennummer: {folgennummer}")
                            # print(f"Folgentitel: {folgentitel_n}")
                    


                # for tit in cont["content"]["titles"]:
                #     print(tit["date"])
            # print(cont["content"]["__type"])
        # print(json_data["props"]["widgets"])
        # print(json_data["props"]["widgets"]["content"])
        # print(len(json_data["props"]["widgets"]))