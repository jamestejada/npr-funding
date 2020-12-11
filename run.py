#! /bin/env python3
import pytest
from modules.output.bot import run_bot
from modules.output.write import write
from modules.input.input_files import download_input_files
from modules.config.settings import BOT_RUN, TESTING

# TO DO:
#   - Clean Up Get_Spreadsheets class
#       - Maybe create on main function within class that
#         calls the other functions.
#   - Figure out how to keep processing even
#     when NPR leaves blanks in their schedule. 
#   - Maybe create classes for processing different spreadsheets. 
#   - Go back to Linux.
#   - Clean up requirements.txt
#   - Clean up imports
#   - Do new version of slack client


def normal_run():
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
