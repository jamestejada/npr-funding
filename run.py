#! /bin/env python3
from modules.output.bot import run_bot
from modules.output.write import write
from modules.input.input_files import download_input_files
from modules.config.settings import BOT_RUN, TESTING


# Change this!!!!!!!!!! to run bot and get input files from windows side
# and then run write from linux side.
# or maybe I should just convert everything to the windows side.

def normal_run():
    download_input_files()
    write()



def main():
    if BOT_RUN:
        run_bot()
    else:
        normal_run()

if __name__=='__main__':
    main()
