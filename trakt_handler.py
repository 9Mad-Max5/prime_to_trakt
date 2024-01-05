import datetime
import os
from trakt import init
import trakt.core 
from trakt.tv import TVShow
from trakt.sync import get_history

from credentials import *

def trakt_auth_handler(username, client_id=None, client_secret=None):
    if not os.path.isfile(os.path.expanduser("~/.pytrakt.json")):
        if not client_id and not client_secret:
            trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH  # Set the auth method to OAuth
            init(username, store=True)
        elif client_id and client_secret:
            trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH  # Set the auth method to OAuth
            init(username, client_id=client_id, client_secret=client_secret, store= True)
    else:
        trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH  # Set the auth method to OAuth



def search_show(show):
    show = None
    min_viewed = 1
    display_crop = 5
    search_res = TVShow.search(show_title)

    if len(search_res) == 1:
        show = search_res[0]
    elif len(search_res) > 1:
        for res in search_res:
            # print(f" {res.title} {res.year} {res.seasons} {res.progress}")
            if res.progress["completed"] >= min_viewed:
                show = res

    if not show:
        print("Es wurde keine passende Serie gefunden bitte wähle aus!")
        for idx, res in enumerate(search_res[:display_crop]):
            print(f"{idx}: {res.title} {res.year}") 

        # Benutzereingabe für die Auswahl
        user_choice = input(f"Bitte wähle eine Nummer (0-{display_crop-1}) für die gewünschte Show: ")

        # Überprüfe, ob die Eingabe eine gültige Nummer ist
        try:
            user_choice = int(user_choice)
            if 0 <= user_choice < display_crop:
                show = search_res[user_choice]
                print(f'Du hast {show.title} {show.year} ausgewählt.')
                # Hier kannst du weitere Aktionen mit der ausgewählten Show durchführen
            else:
                print(f"Ungültige Auswahl. Bitte wähle eine Nummer zwischen 0 und {display_crop-1}.")
        except ValueError:
            print("Ungültige Eingabe. Bitte gib eine Nummer ein.")

    return show

def mark_episode(show, season, episode):
    for c_s in show.seasons:
        if c_s.season == season_number:
            season = c_s

    for ep in season.episodes:
        if ep.number == episode_number:
            episode = ep

    watched = get_history(episode)
    if not watched:
        episode.mark_as_seen()
        print(f"Marked as seen: {episode}")


# Beispielinformationen für die Geschichte
show_title = 'INVINCIBLE'
season_number = 2
episode_number = 2
watched_date = datetime.datetime.now()

trakt_auth_handler(tr_username)
c_show = search_show(show_title)
mark_episode(c_show, season_number, episode_number)
# print(f'Successfully added {show_title} Season {season_number} Episode {episode_number} to your Trakt history.')
