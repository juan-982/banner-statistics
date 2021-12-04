import os, re
import utils.http_client as http_client

from urllib.parse import urlparse, parse_qsl, urlencode, unquote

_LOG_PATH = os.environ["USERPROFILE"] + "/AppData/LocalLow/miHoYo/Genshin Impact/output_log.txt"
_REGEX = "^OnGetWebViewPageFinish:https:\/\/webstatic-sea\.mihoyo\.com\/hk4e\/event\/.*\/log$"

_GACHA_TYPES = {
    "beginner": "100",
    "standard": "200",
    "character": "301",
    "weapon": "302",
    }

def index(gacha_type, page, end_id=0, size=20):
    log = None

    with open(_LOG_PATH, "r") as log_file:
        for line in log_file: # Go through the lines one at a time
            m = re.match(_REGEX, line) # Check each line
            if m: # If we have a match...
                log = line
               
    url = urlparse(log.replace("OnGetWebViewPageFinish:", "", 1))
    url = url._replace(netloc="hk4e-api-os.mihoyo.com", path="event/gacha_info/api/getGachaLog")

    response = http_client.get(url.geturl())

    return response.json()
