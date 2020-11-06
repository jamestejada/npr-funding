import pytest
import pandas as pd
from pathlib import Path
from modules.processing.cut_converter import (
    sheet_ingest, get_id_cut_number_converter, process_columns
    )
from tests.fixtures import news_file, full_target_data


def test_get_id_cut_number_converter(news_file, full_target_data):
    assert get_id_cut_number_converter(news_file) == full_target_data


def test_process_columns(news_file, full_target_data):
    for sheet, row_pairs in sheet_ingest.items():
        df = pd.read_excel(news_file, sheet)
        for each_pair in row_pairs:
            one_dict = process_columns(df, *each_pair)
            for seg_code, cut_no in one_dict.items():
                assert full_target_data[seg_code] == cut_no
