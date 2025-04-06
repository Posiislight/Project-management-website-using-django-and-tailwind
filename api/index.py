from django.core.wsgi import get_wsgi_application
from mangum import Mangum  # Optional, for ASGI
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

app = get_wsgi_application()
