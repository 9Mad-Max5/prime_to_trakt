from trakt import init
import trakt.core
from credentials import *

if tr_username:
    if not CLIENT_ID and not CLIENT_SECRET:
        trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH  # Set the auth method to OAuth
        init(tr_username, store=True)
    elif CLIENT_ID and CLIENT_SECRET:
        init(tr_username, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, store=True)