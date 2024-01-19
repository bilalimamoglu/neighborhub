from dotenv import load_dotenv
import os

load_dotenv()

EVENTS_URL = os.getenv("EVENTS_URL")
CALENDAR_RESOURCES_URL = os.getenv("CALENDAR_RESOURCES_URL")
CONTROL_VARIABLES_URL = os.getenv("CONTROL_VARIABLES_URL")
LOGO_PATH = os.path.join('resources', 'asset.png')