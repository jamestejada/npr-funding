import pytest
from modules.config.settings import (
    REGULAR_FUNDING_CREDITS, NEWSCAST_FUNDING_CREDITS, FULL_SORTED_LIST
)
from modules.processing.funding_credit_schedule import get_time_to_cutid_converter
from tests.fixtures import news_file, newscast_file, cut_id_converter, time_to_cutid_converter


def test_get_time_to_cutid_converter(news_file, newscast_file, time_to_cutid_converter):
    assert time_to_cutid_converter == get_time_to_cutid_converter(news_file, newscast_file)
    