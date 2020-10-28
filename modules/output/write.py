from modules.processing.funding_credit_schedule import get_time_to_cutid_converter
from modules.output.output import Funding_Credit_Output
from modules.config.settings import NEWS_FILE, NEWSCAST_FILE, OUTPUT_FILE


def write():
    time_id_converter = get_time_to_cutid_converter(NEWS_FILE, NEWSCAST_FILE)
    
    output_df = Funding_Credit_Output(time_id_converter)
        # if not write_to.lower().strip() == 'excel':
    print('Writing to Excel...')
    output_df.write_to_excel(OUTPUT_FILE)
        
        # if not write_to.lower().strip() == 'sheets':
    print('Writing to Google Sheets...')
    output_df.write_to_google_sheets()