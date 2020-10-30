import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime


ENV_PATH = Path.cwd().joinpath('modules', 'config', '.env')
load_dotenv(dotenv_path=ENV_PATH)


def check_flags(flags) -> bool:
    for arg in flags:
        if arg in sys.argv[1:]:
            return True
    return False


SLACK_TOKEN = os.getenv('SLACK_TOKEN')

TESTING = check_flags(['testing', 'test'])
BOT_RUN = check_flags(['bot', 'app'])

TEST_DATA = Path.cwd().joinpath('tests', 'data')
TRUE_DATA = Path.cwd().joinpath('data')
DATA = TEST_DATA if TESTING else TRUE_DATA

NEWS_FILE = DATA.joinpath('news.xls')
NEWSCAST_FILE = DATA.joinpath('newscast.xls')
now = datetime.now().strftime('%Y%m%d')
OUTPUT_FILE = DATA.joinpath(f'output{now}.xlsx')

TARGET_SHEET = os.getenv('TEST_ID' if TESTING else 'SPREADSHEET_ID')
CRED_PATH = Path.cwd().joinpath('modules', 'config', 'credentials.json')
TOKEN_PATH = Path.cwd().joinpath('modules', 'config', 'token.pickle')

# For NPR Stations website
USER_NAME = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
LOGIN_PAGE = os.getenv('LOGIN_PAGE')
CREDIT_PAGE = os.getenv('CREDIT_PAGE')

DOWNLOAD_FOLDER = Path('C:\\Users\\james.tejada\\Downloads')
DOWNLOAD_PATH_NEWS = DOWNLOAD_FOLDER.joinpath('news.xls')
DOWNLOAD_PATH_NEWSCAST = DOWNLOAD_FOLDER.joinpath('newscast.xls')
