import os

from dotenv import load_dotenv


load_dotenv()

TG_TOKEN = os.environ.get('TOKEN')
DATABASE_URL = os.environ.get('DATABASE_URL')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
POLLING_MODE = os.environ.get('POLLING_MODE') is True
SITE_URL = os.environ.get('SITE_URL')