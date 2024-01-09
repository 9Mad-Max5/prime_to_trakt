class Episode:
    def __init__(self, nummer, titel, datum):
        self.nummer = nummer
        self.titel = titel
        self.datum = datum

class Staffel:
    def __init__(self, name):
        self.name = name
        self.episoden = {}

    def add_episode(self, nummer, titel, datum):
        # Überprüfen, ob die Episode bereits existiert
        if nummer not in self.episoden:
            self.episoden[nummer] = Episode(nummer, titel, datum)

class Serie:
    """A Class representing a TV Show object."""
    def __init__(self, name):
        self.name = name
        self.staffeln = {}

    def add_staffel(self, staffel):
        # Überprüfen, ob die Staffel bereits existiert
        if staffel not in self.staffeln:
            self.staffeln[staffel] = Staffel(staffel)

class Film:
    """A Class representing a Movie object."""
    def __init__(self, name, datum):
        self.name = name
        self.datum = datum
