from pathlib import Path
import requests
from bs4 import BeautifulSoup
from funder.modules.config.settings import (
    USER_NAME, PASSWORD, LOGIN_PAGE, CREDIT_PAGE, NPR_ROOT,
    NEWS_FILE, NEWSCAST_FILE
)


class Get_Spreadsheets:
    """Scrapes the NPR Stations website to download 
    two Excel input files needed for funding credits"""
    USER_AGENT = {
        'User-Agent': 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' 
        + 'Chrome/87.0.4280.66 Safari/537.36'
    }

    # pages
    NPR_ROOT = NPR_ROOT
    LOGIN_PAGE = LOGIN_PAGE
    CREDIT_PAGE = CREDIT_PAGE

    LINK_TEXTS = ['News', 'Newscasts']

    OUTPUT_FILE = {
        'News': NEWS_FILE,
        'Newscasts': NEWSCAST_FILE
    }

    def __init__(self, username=None, password=None):
        self.params = {
            'loginUrl': False,
            'dologin': True,
            'username': USER_NAME,
            'password': PASSWORD
        }
        self.session = requests.Session()

    # main
    def download(self):
        """Main method for Get_Spreadsheets class"""
        self.send(self.login, 'Logging in to NPR Stations...')
        funding_response = self.send(
            self.funding_credits_page, 'Accessing Funding Credits Page...'
            )
        href_list = self.find_links(funding_response.text)
        try:
            assert len(href_list) == 2, f'href_list is not right: {len(href_list)}'
        except AssertionError as e:
            print(e)

        for link, link_text in href_list:
            download_url = self.one_download_page(link, link_text)
            self.send(
                self.download_one_file,
                f'Saving {link_text} File...',
                download_url, link_text
                )
    
    def login(self):
        """Logs into NPR stations website"""
        return self.session.post(self.LOGIN_PAGE, params=self.params, headers=self.USER_AGENT)
    
    def funding_credits_page(self):
        """Gets NPR funding credits page"""
        return self.session.get(self.CREDIT_PAGE, headers=self.USER_AGENT)

    def find_links(self, funding_credit_html):
        """Finds full url for download pages based on the display text of links 
        (e.g. 'Newscasts', or 'News'). This returns a list of tuples. Each tuple
        consists of the full url paired with the link text"""
        soup = BeautifulSoup(funding_credit_html, 'html.parser')
        hrefs = [
                (self.full_link(link), link_text)   # tuple
                for link in soup.find_all('a') 
                if (link_text := str(link.text).strip()) in self.LINK_TEXTS
            ]
        return hrefs
    
    def full_link(self, partial_link):
        """appends the root address to the relative href from page links to create
        the full url. Used by self.find_linkes()"""
        return f'{self.NPR_ROOT}{partial_link.get("href")}'

    def one_download_page(self, dl_page_link, link_text):
        """returns to the direct url to one excel file."""
        download_page = self.session.get(dl_page_link, headers=self.USER_AGENT)
        soup = BeautifulSoup(download_page.text, 'html.parser')
        return f'{self.NPR_ROOT}{soup.a.get("href")}'
    
    def download_one_file(self, download_url, link_text):
        """Downloads a spreadsheet file"""
        download_response = self.session.get(download_url, headers=self.USER_AGENT)
    
        output_path = self.OUTPUT_FILE.get(link_text)
        with open(output_path, 'wb') as outfile:
            outfile.write(download_response.content)
        return download_response

    def send(self, request_func, print_string, *args):
        """A request function decorator without the decoration.
        This method prints what the class is doing at the moment
        (contained in print_string) with a SUCCESS or FAILED message
        depending on response status code from the request."""
        print(print_string, end='\r')

        response = request_func(*args)
        result = 'SUCCESS' if 200 == response.status_code else 'FAILED'

        print(print_string, result)
        return response


# Main
def download_input_files():
    sheets = Get_Spreadsheets()
    sheets.download()