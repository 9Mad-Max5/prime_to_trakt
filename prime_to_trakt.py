from classes import *
from credentials import *
from service_functions import *
from prime_parser import *
from prime_crawler import *
from trakt_handler import *

page = "https://www.amazon.com/gp/video/settings/watch-history"

# # Pfad zum aktuellen Skript
# script_path = os.path.abspath(sys.argv[0])
# sel_timeout = 60


soup = crawl_amazon(page=page, username=username, password=password, totp=totp)
serien = parse_infos(soup=soup)

print(serien)
