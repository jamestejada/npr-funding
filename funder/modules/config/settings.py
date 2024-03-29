import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime


ENV_PATH = Path.cwd().joinpath('funder', 'modules', 'config', '.env')
load_dotenv(dotenv_path=ENV_PATH)


def from_cwd(*path_list):
    directory = Path.cwd().joinpath(*path_list)
    directory.mkdir(exist_ok=True, parents=True)
    return directory


def check_flags(flags) -> bool:
    return any([(arg in flags) for arg in sys.argv[1:]])


SLACK_TOKEN = os.getenv('SLACK_TOKEN')

WRITE = check_flags(['write', 'process'])
TESTING = check_flags(['testing', 'test', 'tests'])
BOT_RUN = check_flags(['bot', 'app'])

TEST_DATA = from_cwd('tests', 'data')
TRUE_DATA = from_cwd('data')
DATA = TEST_DATA if TESTING else TRUE_DATA

NEWS_FILE = DATA.joinpath('news.xls')
NEWSCAST_FILE = DATA.joinpath('newscast.xls')
now = datetime.now().strftime('%Y%m%d')
OUTPUT_FILE = DATA.joinpath(f'output{now}.xlsx')

TARGET_SHEET = os.getenv('TEST_ID' if TESTING else 'SPREADSHEET_ID')
_CONFIG_PATH = from_cwd('funder', 'modules', 'config')
CRED_PATH = _CONFIG_PATH.joinpath('credentials.json')

# For NPR Stations website
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
NPR_ROOT = os.getenv('NPR_ROOT')
LOGIN_PAGE = f'{NPR_ROOT}{os.getenv("LOGIN_PAGE")}'
CREDIT_PAGE = f'{NPR_ROOT}{os.getenv("CREDIT_PAGE")}'


REGULAR_FUNDING_CREDITS = [
    '4:45',
    '5:21', '5:34', '5:45',
    '6:21', '6:34', '6:45',
    '7:21', '7:34', '7:45',
    '8:21', '8:34', '8:45',
    '15:35', '15:58',
    '16:20', '16:35', '16:58',
    '17:20', '17:35', '17:58',
    '18:20'
]

NEWSCAST_FUNDING_CREDITS = [
    '5:05', '6:05', '7:05',
    '8:05', '9:05',

    # For Fund Drive
    '10:05', '11:05', '12:05', '13:05',

    '14:05', '15:05', '16:05',
    '17:05', '18:05'
]

FULL_SORTED_LIST = [
    '4:45',
    '5:05', '5:21', '5:34', '5:45',
    '6:05', '6:21', '6:34', '6:45',
    '7:05', '7:21', '7:34', '7:45',
    '8:05', '8:21', '8:34', '8:45',
    '9:05',
    
    # For Fund Drive
    '10:05', '11:05', '12:05', '13:05',
    
    '14:05', '15:05', '15:35', '15:58',
    '16:05', '16:20', '16:35', '16:58',
    '17:05', '17:20', '17:35', '17:58',
    '18:05', '18:20'
]
