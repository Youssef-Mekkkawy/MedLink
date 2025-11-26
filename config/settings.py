"""Auto-generated file: settings.py"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ATTACHMENTS_DIR = BASE_DIR / "attachments"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
ATTACHMENTS_DIR.mkdir(exist_ok=True)
(ATTACHMENTS_DIR / "prescriptions").mkdir(exist_ok=True)
(ATTACHMENTS_DIR / "lab_results").mkdir(exist_ok=True)
(ATTACHMENTS_DIR / "xrays").mkdir(exist_ok=True)
(ATTACHMENTS_DIR / "reports").mkdir(exist_ok=True)

# App metadata
APP_NAME = "MedLink"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Unified Medical Records System"

# Window settings
WINDOW_SIZE = "1400x800"
MIN_WINDOW_SIZE = (1200, 700)

# Session settings
SESSION_TIMEOUT = 30  # minutes

# Date format
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
