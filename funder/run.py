#! /bin/env python3
import pytest
from funder.modules.output.bot import run_bot
from funder.modules.output.write import write
from funder.modules.input.input_files import download_input_files
from funder.modules.config.settings import BOT_RUN, TESTING, WRITE

# TO DO:
#   - Clean Up Get_Spreadsheets class
#   ** - Maybe create classes for processing different spreadsheets. 
#           - It is getting hard to track functions in funding_credit_schedule.py.
#           - Clean up 
#   - Clean up requirements.txt
#   - Clean up imports
#   - Do new version of slack client


def normal_run():
    if not WRITE:
        download_input_files()
    write()


def main():
    if TESTING:
        pytest.main(['-vv'])
    elif BOT_RUN:
        run_bot()
    else:
        normal_run()


if __name__=='__main__':
    main()
