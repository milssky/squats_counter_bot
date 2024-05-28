import os

from dotenv import load_dotenv


load_dotenv()

TG_TOKEN = os.environ.get('TOKEN')
DATABASE_URL = os.environ.get('DATABASE_URL')