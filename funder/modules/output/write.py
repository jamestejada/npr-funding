from funder.modules.processing.funding_credit_schedule import get_time_to_cutid_converter
from funder.modules.output.output import Funding_Credit_Output
from funder.modules.config.settings import NEWS_FILE, NEWSCAST_FILE, OUTPUT_FILE


def write():

    time_id_converter = get_time_to_cutid_converter(NEWS_FILE, NEWSCAST_FILE)
    
    output_df = Funding_Credit_Output(time_id_converter)

    print('Writing to Excel...')
    output_df.write_to_excel(OUTPUT_FILE)

    print('Writing to Google Sheets...')
    output_df.write_to_google_sheets()