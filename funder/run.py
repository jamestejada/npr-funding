#! /bin/env python3
import pytest
from funder.modules.output.bot import run_bot
from funder.modules.output.write import write
from funder.modules.input.input_files import download_input_files
from funder.modules.config.settings import BOT_RUN, TESTING, WRITE

# TO DO:
#   - Clean Up Get_Spreadsheets class
#       - Maybe create on main function within class that
#         calls the other functions.
#   DONE - Figure out how to keep processing even
#     when NPR leaves blanks in their schedule. 
#   - Maybe create classes for processing different spreadsheets. 
#   DONE - Go back to Linux. NOTE: problems arose when using linux because
#          I set an environment variable in '.env' as "USER" which ended up returning
#          the linux user name instead of the username in '.env.' "USER_NAME" is now used
#          to fix this.
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
