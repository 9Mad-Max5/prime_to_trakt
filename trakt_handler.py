import os
from trakt import init
import trakt.core
from trakt.tv import TVShow, studios
from trakt.movies import Movie
from trakt.sync import get_history
from time import sleep
from credentials import *
from classes import *


def trakt_auth_handler(username, client_id=None, client_secret=None):
    if not os.path.isfile(os.path.expanduser("~/.pytrakt.json")):
        if not client_id and not client_secret:
            trakt.core.AUTH_METHOD = (
                trakt.core.OAUTH_AUTH
            )  # Set the auth method to OAuth
            init(username, store=True)
        elif client_id and client_secret:
            trakt.core.AUTH_METHOD = (
                trakt.core.OAUTH_AUTH
            )  # Set the auth method to OAuth
            init(username, client_id=client_id, client_secret=client_secret, store=True)
    else:
        trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH  # Set the auth method to OAuth


def search_show(show_title, silent):
    show = None
    min_viewed = 1
    display_crop = 5
    search_res = TVShow.search(show_title)

    if len(search_res) == 1:
        show = search_res[0]
    elif len(search_res) > 1:
        for res in search_res:
            if res.progress["completed"] >= min_viewed:
                show = res
                break

        if not show:
            az_studios = ['Amazon Studios', '3 Arts Entertainment']
            for res in search_res:
                l_studios = studios(res)
                for studio in l_studios:
                    for az_studio in az_studios:
                        if az_studio in studio["name"]:
                            show = res
                            break

    if not show:
        if silent == True:
            show = None

        elif len(search_res) > 0:
            if len(search_res) < display_crop:
                display_crop = len(search_res)

            print(
                f"Zu {show_title} wurde keine passende Serie gefunden bitte wähle aus!"
            )
            for idx, res in enumerate(search_res[:display_crop]):
                print(f"{idx+1}: {res.title} {res.year}")

            # Benutzereingabe für die Auswahl
            user_choice = input(
                f"Bitte wähle eine Nummer (1-{display_crop}) für die gewünschte Show: "
            )

            # Überprüfe, ob die Eingabe eine gültige Nummer ist
            try:
                user_choice = int(user_choice)-1
                if 0 <= user_choice < display_crop:
                    show = search_res[user_choice]
                    print(f"Du hast {show.title} {show.year} ausgewählt.")
                    # Hier kannst du weitere Aktionen mit der ausgewählten Show durchführen
                else:
                    print(
                        f"Ungültige Auswahl. Bitte wähle eine Nummer zwischen 0 und {display_crop-1}."
                    )
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Nummer ein.")

        else:
            show = None

    return show

def search_movie(movie_title, silent):
    movie = None
    min_viewed = 1
    display_crop = 5
    search_res = Movie.search(movie_title)

    if len(search_res) == 1:
        movie = search_res[0]
        
        if not movie:
            az_studios = ['Amazon Studios', '3 Arts Entertainment']
            for res in search_res:
                l_studios = studios(res)
                for studio in l_studios:
                    for az_studio in az_studios:
                        if az_studio in studio["name"]:
                            movie = res
                            break

    if not movie:
        if silent == True:
            movie = None

        elif len(search_res) > 0:
            if len(search_res) < display_crop:
                display_crop = len(search_res)

            print(
                f"Zu {movie_title} wurde keine passende Serie gefunden bitte wähle aus!"
            )
            for idx, res in enumerate(search_res[:display_crop]):
                print(f"{idx+1}: {res.title} {res.year}")

            # Benutzereingabe für die Auswahl
            user_choice = input(
                f"Bitte wähle eine Nummer (1-{display_crop}) für den gewünschten Film: "
            )

            # Überprüfe, ob die Eingabe eine gültige Nummer ist
            try:
                user_choice = int(user_choice)-1
                if 0 <= user_choice < display_crop:
                    movie = search_res[user_choice]
                    print(f"Du hast {movie.title} {movie.year} ausgewählt.")
                    # Hier kannst du weitere Aktionen mit der ausgewählten Show durchführen
                else:
                    print(
                        f"Ungültige Auswahl. Bitte wähle eine Nummer zwischen 0 und {display_crop-1}."
                    )
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Nummer ein.")

        else:
            movie = None

    return movie

def mark_episode(show, season, episode, watched_at):
    for c_s in show.seasons:
        if int(c_s.season) == int(season):
            c_season = c_s
            for ep in c_season.episodes:
                if int(ep.number) == int(episode):
                    c_episode = ep
                    watched = get_history(c_episode)
                    if not watched:
                        c_episode.mark_as_seen(watched_at)
                        print(f"Marked as seen: {c_episode}")
                        sleep(1)
                        break

def mark_movie(movie, watched_at):
    watched = get_history(movie)
    if not watched:
        movie.mark_as_seen(watched_at)
        print(f"Marked as seen: {movie}")
        sleep(1)

def import_dict(dictionary, tr_username, silent=True):
    """
    Connection point to prime to trakt.
    Retrieves the collected data dictonary and calls the needed Funktions.
    """
    trakt_auth_handler(tr_username)
    # if isinstance(dictionary[0], Serie):
    if all(issubclass(type(element), Serie) for element in dictionary.values()):
        for _show in dictionary:
            show = dictionary[_show]
            c_show = search_show(_show, silent)
            if c_show:
                for _season in show.staffeln:
                    season = show.staffeln[_season]
                    for _eps in season.episoden:
                        episode = season.episoden[_eps]
                        # print(show.name, season.name, episode.nummer, episode.datum)
                        mark_episode(c_show, season.name, episode.nummer, episode.datum)

    # elif isinstance(dictionary[0], Film):
    elif all(issubclass(type(element), Film) for element in dictionary.values()):
        for _movie in dictionary:
            movie = dictionary[_movie]
            c_movie = search_movie(_movie, silent)
            if c_movie:
                mark_movie(c_movie, movie.datum)
