import os
import sys

# Ensure root directory is on Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app

# Vercel WSGI entry point
# Flask `app` is exposed as the callable
