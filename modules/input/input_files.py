import os
import time
import shutil
import helium as he
from selenium.webdriver.chrome.options import Options
from modules.config.settings import (
    USER_NAME, PASSWORD, DOWNLOAD_PATH_NEWS,
    LOGIN_PAGE, CREDIT_PAGE,
    DOWNLOAD_PATH_NEWSCAST, TRUE_DATA
    )


# main
def download_input_files():
    helium_driver = login()
    get_file_links(helium_driver)


def login():

    print('Logging in to NPR stations...')
    he.start_chrome(LOGIN_PAGE)
    he.write(USER_NAME, into='User Name')
    he.press(he.Keys.TAB)
    he.write(PASSWORD)
    he.press(he.Keys.TAB)
    he.get_driver().find_element_by_xpath('//*[@id="login"]/div[3]/input').click()

    return he


def get_file_links(helium_driver):
    try:
        for link_text in ['News', 'Newscasts']:
            print(f"Getting {link_text} link...")
            helium_driver.go_to(CREDIT_PAGE)
            get_one_link(helium_driver, link_text)
    except Exception as e:
        print(e)
    finally:
        helium_driver.kill_browser()


def get_one_link(helium_driver, link_text):

    link_elem = helium_driver.get_driver().find_element_by_link_text(link_text)
    link_href = link_elem.get_attribute('href')
    local_path = download_one(helium_driver, link_href, link_text)
    transfer_to_data(link_text, local_path)


def transfer_to_data(link_text, download_path):

    data_path = TRUE_DATA.joinpath(
        {
            'News': 'news.xls',
            'Newscasts': 'newscast.xls'
        }.get(link_text)
    )

    shutil.copy( str(download_path.absolute()), str(data_path.absolute()))

    print(f'{link_text} file transferred...')

    os.remove(download_path)


def download_one(helium_driver, link_href, link_text):

    local_path = {
        'News': DOWNLOAD_PATH_NEWS,
        'Newscasts': DOWNLOAD_PATH_NEWSCAST
        }.get(link_text)

    helium_driver.go_to(link_href)

    while not local_path.exists():
        time.sleep(1)

    print(f'{link_text} file downloaded...')

    return local_path
