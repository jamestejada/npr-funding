import pandas as pd
from pandas import ExcelWriter
from dateutil.parser import parse
from funder.modules.config.settings import (
    CRED_PATH, TOKEN_PATH, TARGET_SHEET, NEWSCAST_FUNDING_CREDITS
    )

# Google stuff
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Funding_Credit_Excel:

    COLUMN_WIDTH = 13
    INSIGHT_NEWSCAST = '9:05'
    ROW_OFFSET = 3
    TIME_HEADER = 'TIME'
    DAY_OF_WEEK_HEADER = ['', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', '']
    SHEET_NAME = 'NPR Funding Credits'

    def __init__(self, dataframe_dictionary):
        self._dataframe = pd.DataFrame.from_dict(dataframe_dictionary)
        self.dataframe = self.process_df()
        self.max_row, self.max_col = self.dataframe.shape
        self.legend_column = self.max_col + 1
        self.highlight_format = {'bold': True, 'align': 'center', 'valign': 'center'}
    
    def write_to_excel(self, output_file):
        with ExcelWriter(output_file, engine='xlsxwriter') as writer:
            self.dataframe.to_excel(
                writer, self.SHEET_NAME, index=False,
                header=False, startrow=self.ROW_OFFSET
            )

            workbook = writer.book
            worksheet = writer.sheets[self.SHEET_NAME]

            self.write_header(worksheet, workbook)
            self.set_column_widths(worksheet)
            self.set_row_height(worksheet)
            self.format_highlights(worksheet, workbook)

    def process_df(self):
        self._dataframe = self._dataframe.reset_index()
            # replaces first element of header row with self.TIME_HEADER
        self.header = [self.TIME_HEADER, *self._dataframe.columns.to_list()[1:]]
        self._dataframe.columns = self.header
        return self._dataframe

    def write_header(self, worksheet, workbook):
        format_header = workbook.add_format(self.highlight_format)
        format_header_with_bottom = workbook.add_format({'bottom': 2, **self.highlight_format})
        for i in range(self.max_col):
            worksheet.write((self.ROW_OFFSET - 2), i, self.DAY_OF_WEEK_HEADER[i], format_header)
        for i in range(self.max_col):
            worksheet.write((self.ROW_OFFSET - 1), i, self.header[i], format_header_with_bottom)

    def add_legend(self, worksheet, workbook, format_green, format_yellow):
        format_header_with_bottom = workbook.add_format({'bottom': 2, **self.highlight_format})
        worksheet.write(10, self.legend_column, 'Color Legend', format_header_with_bottom)
        worksheet.write(11, self.legend_column, 'Newscasts', format_green)
        worksheet.write(12, self.legend_column, 'Insight', format_yellow)


    def format_highlights(self, worksheet, workbook):
        format_green = workbook.add_format({'bg_color': '#A9D08E', **self.highlight_format})
        format_yellow = workbook.add_format({'bg_color': '#FFFF99', **self.highlight_format})
        format_normal = workbook.add_format({'align': 'center'})

        self.add_legend(worksheet, workbook, format_green, format_yellow)

        for index, time in enumerate(self.dataframe[self.TIME_HEADER]):

            row_number = index + self.ROW_OFFSET

            if time == self.INSIGHT_NEWSCAST:
                for i in range(self.max_col):
                    worksheet.write(row_number, i, self.dataframe.iloc[index, i], format_yellow)
            elif time in NEWSCAST_FUNDING_CREDITS:
                for i in range(self.max_col):
                    worksheet.write(row_number, i, self.dataframe.iloc[index, i], format_green)
            else:
                for i in range(self.max_col):
                    worksheet.write(row_number, i, self.dataframe.iloc[index, i], format_normal)

    
    def set_column_widths(self, worksheet):
        # Time Column (thinner)
        worksheet.set_column(0, 8)
        # Source Column (thinner)
        worksheet.set_column((self.max_col - 1), 8)
        # Standard columns with cut numbers
        worksheet.set_column(1, (self.max_col - 2), self.COLUMN_WIDTH)
        # Legend Column
        worksheet.set_column(self.legend_column, self.legend_column, self.COLUMN_WIDTH)

    def set_row_height(self, worksheet):
        worksheet.set_row(0, 30)
        for row in range(self.max_row + self.ROW_OFFSET + 1):
            worksheet.set_row(row, 20)

    def write_to_google_sheets(self):
        """ For the future!
        """
        raise NotImplementedError

    def __str__(self):
        return str(self.dataframe)


class Funding_Credit_Output(Funding_Credit_Excel):

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    SPREADSHEET_ID = TARGET_SHEET
    VALUE_INPUT_OPTION = 'RAW'

    def __init__(self, dataframe_dictionary):
        super().__init__(dataframe_dictionary)
        self.credentials = self.get_google_credentials()
        self.blank_row = ['' for _ in range(self.max_col)]
        self.value_range_body = {'values': self.build_row_list()}
        self._service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self._service.spreadsheets()
        self.week_of = self.get_first_date()

    def write_to_google_sheets(self):
        self.update_sheet_name()

        return self.sheet.values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=self.SHEET_NAME,
            valueInputOption=self.VALUE_INPUT_OPTION,
            body=self.value_range_body
        ).execute()

    def update_sheet_name(self):
        requests = [{
            'updateSpreadsheetProperties': {
                'properties': {
                    'title': f'NPR Funding Credit Sked Week of {self.week_of}'
                },
                'fields': 'title'
            }
        }]
        body = {'requests': requests}

        return self.sheet.batchUpdate(
            spreadsheetId=self.SPREADSHEET_ID, body=body
            ).execute()

    def get_first_date(self):
        first_datetime = parse(self.dataframe.columns.to_list()[1])
        return first_datetime.strftime('%#m/%#d/%y')

    def build_row_list(self):
        row_list = [self.blank_row for _ in range(self.ROW_OFFSET - 2)] # Add blank rows
        row_list.append(self.DAY_OF_WEEK_HEADER)
        row_list.append(self.header)

        for index, row in self.dataframe.iterrows():
            row_list.append([row[self.header[i]] for i in range(self.max_col)])
        return row_list

    def get_google_credentials(self):
        creds = None
        if TOKEN_PATH.exists():
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CRED_PATH, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        return creds