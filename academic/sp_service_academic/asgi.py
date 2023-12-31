"""
ASGI config for sp_service_academic project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv('./.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sp_service_academic.settings.production')

application = get_asgi_application()
