import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMPLATES_DIR = BASE_DIR / 'templates'
CLIENT_DIR = BASE_DIR / 'client'
BUILD_DIR = CLIENT_DIR / 'build'

CORS_ORIGIN = None

DEBUG = False

"""
# USER MODEL
"""

AUTH_USER_MODEL = 'miq.User'