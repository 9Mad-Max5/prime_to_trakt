from classes import *
from credentials import *
from service_functions import *
from prime_parser import *
from prime_crawler import *
from trakt_handler import *

page = "https://www.amazon.com/gp/video/settings/watch-history"

# script_path = os.path.abspath(sys.argv[0])


soup = crawl_amazon(page=page, username=username, password=password, totp=totp)
serien = parse_tv(soup=soup)
filme = parse_movie(soup=soup)

# import_dict(serien, tr_username, silent=False)
import_dict(filme, tr_username, silent=False)
