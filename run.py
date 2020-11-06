#! /bin/env python3
import pytest
from modules.output.bot import run_bot
from modules.output.write import write
from modules.input.input_files import download_input_files
from modules.config.settings import BOT_RUN, TESTING

# temp
from modules.processing.cut_converter import get_id_cut_number_converter, process_columns
from pathlib import Path


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
