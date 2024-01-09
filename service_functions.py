import re
from translation_dict import prime_replace_naming

def sanatize(title):
    sanatizer = [" [dt./OV]", " [OV]", " [OV/OmU]"]
    for s in sanatizer:
        if s in title:
            bereinigter_titel = title.replace(s, '')
            break
    return bereinigter_titel


def extract_ser_sn(name):
    # Definiere das Muster für den Serientitel und die Staffelnummer
    muster = [
        re.compile(r"(.+) – Staffel (\d+)"),
        re.compile(r"(.+) - Staffel (\d+)"),
        re.compile(r"(.+) - Season (\d+)"),
        re.compile(r"(.+) Staffel (\d+)"),
    ]

    if name in prime_replace_naming:
        name = prime_replace_naming[name]

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
        staffelnummer = 0
    else:
        print(f"Kein Seriennamen gefunden: {name}")

    return serientitel, staffelnummer


def extract_epsn_en(name):
    # Definiere das Muster für die Folgennummer und den Folgentitel
    muster = re.compile(r"Folge (\d+): (.+)")

    # Suche nach Übereinstimmungen im Folgennamen
    ergebnis = muster.match(name)

    folgennummer, folgentitel = None, None
    if ergebnis:
        folgennummer = ergebnis.group(1).zfill(
            2
        )  # Fülle mit Nullen auf, um sicherzustellen, dass die Nummer zwei Stellen hat
        folgentitel = ergebnis.group(2)
        # print(f"Folgennummer: {folgennummer}")
        # print(f"Folgentitel: {folgentitel}")
    else:
        print(f"Keine Nummer gefunden: {name}")

    return folgennummer, folgentitel
