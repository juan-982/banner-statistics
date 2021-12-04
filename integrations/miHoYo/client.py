import os, re, time
import utils.http_client as http_client

from datetime import datetime
from models.wish import Wish
from urllib.parse import urlparse, parse_qsl, urlencode

_LOG_PATH = os.environ["USERPROFILE"] + "/AppData/LocalLow/miHoYo/Genshin Impact/output_log.txt"
_REGEX = "^OnGetWebViewPageFinish:https:\/\/webstatic-sea\.mihoyo\.com\/hk4e\/event\/.*\/log$"
_LAST_VISIT = None

def index(gacha_type, page=1, end_id="0", size=20):
    global _LAST_VISIT
    log = None

    with open(_LOG_PATH, "r") as log_file:
        for line in log_file: # Go through the lines one at a time
            m = re.match(_REGEX, line) # Check each line
            if m: # If we have a match...
                log = line
               
    if log is None:
        raise Exception("Unable to find matching log") 
    
    url = urlparse(log.replace("OnGetWebViewPageFinish:", "", 1))

    params = dict(parse_qsl(url.query))
    params.update(
        {
            "lang": "en-us", 
            "size": size, 
            "gacha_type": Wish.GACHA_TYPES[gacha_type], 
            "page": page, 
            "end_id": end_id
            }
        )

    url = url._replace(netloc="hk4e-api-os.mihoyo.com", path="event/gacha_info/api/getGachaLog", query=urlencode(params), fragment="")

    if _LAST_VISIT is not None and abs((datetime.now() - _LAST_VISIT).total_seconds()) < 3:
        time.sleep(3)

    _LAST_VISIT = datetime.now()
    response = http_client.get(url.geturl())

    return response.json()
