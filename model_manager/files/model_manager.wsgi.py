"""
WSGI config for model_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "model_manager.settings.base")

application = get_wsgi_application()

