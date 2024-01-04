import datetime
from pytrakt import Trakt
from pytrakt.objects import Episode

from credentials import *

# Trakt-Authentifizierung
Trakt.configuration.defaults.client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
Trakt.configuration.defaults.oauth_from_response(token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

# Beispielinformationen für die Geschichte
show_title = 'INVINCIBLE'
season_number = 2
episode_number = 3
watched_date = datetime.datetime.now()

# Erstelle ein Episode-Objekt
episode = Episode(title=show_title, season=season_number, episode=episode_number)

# Füge zur Trakt-Geschichte hinzu
Trakt['sync/history'].add_to_history(episodes=[episode], watched_at=watched_date)

print(f'Successfully added {show_title} Season {season_number} Episode {episode_number} to your Trakt history.')
