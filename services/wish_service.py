import os, re, sqlite3
import utils.db_manager as db_manager
import utils.http_client as http_client
from models.wish import Wish
from urllib.parse import urlparse, parse_qsl, urlencode, unquote

_LOG_PATH = os.environ["USERPROFILE"] + "/AppData/LocalLow/miHoYo/Genshin Impact/output_log.txt"
_REGEX = "^OnGetWebViewPageFinish:https:\/\/webstatic-sea\.mihoyo\.com\/hk4e\/event\/.*\/log$"

def retrieve_history():
    log = None

    with open(_LOG_PATH, "r") as log_file:
        for line in log_file: # Go through the lines one at a time
            m = re.match(_REGEX, line) # Check each line
            if m: # If we have a match...
                log = line
               
    url = urlparse(log.replace("OnGetWebViewPageFinish:", "", 1))
    
    params = dict(parse_qsl(url.query))
    params.update({"lang": "en-us", "size": 20})
    params.update({"gacha_type": "301"})
    params.update({"page": 1})
    params.update({"end_id": 0})

    url = url._replace(netloc="hk4e-api-os.mihoyo.com", path="event/gacha_info/api/getGachaLog", query=urlencode(params), fragment="")
       
    response = http_client.get(url.geturl())
	

def create(external_id, time, name, gacha_type, item_type, rank_type):
    cursor = sqlite3.connect(db_manager.DB_PATH).cursor()
    cursor.execute("""
      INSERT INTO wishes (external_id, time, name, gacha_type, item_type, rank_type) VALUES(?, ?, ?, ?, ?)
    """, (external_id, time, name, gacha_type, item_type, rank_type))

def list(gacha_type):
    cursor = sqlite3.connect(db_manager.DB_PATH).cursor()
    cursor.execute("""
      SELECT id, external_id, time, name, gacha_type, item_type, rank_type
        FROM wishes
        WHERE gacha_type = ?
    """, gacha_type)
    records = cursor.fetchall()

    wishes = []

    for record in records:
      wishes.append(Wish(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))

    return wishes
