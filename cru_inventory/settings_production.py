from .settings_general import *

DEBUG = False

ALLOWED_HOSTS = ["ianmann56.pythonanywhere.com"]

URL_BASE = "/"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_SSL', 'on')

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
