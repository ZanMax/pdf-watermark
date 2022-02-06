import json

import requests

from app.core.config import SITE_HEALTH_URL


def site_health_check(site_name):
    r = requests.get(f'https://{site_name}/{SITE_HEALTH_URL}')
    result = json.loads(r.text)
    return result
