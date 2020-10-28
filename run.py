#! /bin/env python3
from modules.output.bot import run_bot
from modules.output.write import write
from modules.input.input_files import download_input_files
from modules.config.settings import BOT_RUN, TESTING


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
