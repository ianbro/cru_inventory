from .settings_general import *

DEBUG = False

URL_BASE = "/apps/centraldesk/"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_SSL', 'on')

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'