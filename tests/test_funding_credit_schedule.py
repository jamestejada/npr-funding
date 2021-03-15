from funder.modules.processing.cut_converter import get_id_cut_number_converter
import platform
import pytest
import datetime
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from funder.modules.config.settings import (
    REGULAR_FUNDING_CREDITS, NEWSCAST_FUNDING_CREDITS, FULL_SORTED_LIST
)
from funder.modules.processing.funding_credit_schedule import (
    get_time_to_cutid_converter, convert_cut_id_to_cut_number,
    sort_output_dict, date_to_string, to_pacific_time, EASTERN_TIMEZONE,
    to_pacific_time_newscasts, clean_header_list
    )
from tests.fixtures import (
    news_file, newscast_file, cut_id_converter, time_to_cutid_converter
    )


def test_get_time_to_cutid_converter(news_file, newscast_file, time_to_cutid_converter):
    assert time_to_cutid_converter == get_time_to_cutid_converter(news_file, newscast_file)


def test_convert_cut_id_to_cut_number(cut_id_converter, news_file):
    real_cut_id_converter = get_id_cut_number_converter(news_file)
    for cut_id in cut_id_converter:
        assert type(convert_cut_id_to_cut_number(cut_id, real_cut_id_converter)) is int
        assert int(cut_id_converter.get(cut_id)) == convert_cut_id_to_cut_number(cut_id, real_cut_id_converter)


def test_sort_output_dict(time_to_cutid_converter):
    # sorted() actually unsorts list of time strings
    full_unsorted_list = sorted(FULL_SORTED_LIST)

    # verify it is unsorted
    assert full_unsorted_list != FULL_SORTED_LIST

    # unsort entire dictionary with full_unsorted_list
    unsorted_dict = {}
    for day, day_dict in time_to_cutid_converter.items():
        unsorted_dict[day] = {time: day_dict.get(time) for time in full_unsorted_list}

    # verify unsorted_dict is actually unsorted
    for (day, day_dict), (uday, uday_dict) in zip(time_to_cutid_converter.items(), unsorted_dict.items()):
        for time, utime in zip(day_dict, uday_dict):
            assert time != utime
    
    # re-sort using sort_output_dict
    sorted_dict = sort_output_dict(unsorted_dict)

    # verify re-sorted
    for (day, day_dict), (uday, uday_dict) in zip(
        time_to_cutid_converter.items(), sorted_dict.items()
        ):
        for time, utime in zip(day_dict, uday_dict):
            assert time == utime


def test_date_to_string(time_to_cutid_converter):
    for date_string in time_to_cutid_converter:
        try:
            datetime_obj = parse(date_string)
            assert datetime_obj.strftime('%d-%b') == date_to_string(datetime_obj)
        except ParserError as e:
            assert date_to_string(date_string) is None

def test_to_pacific_time():

    today = datetime.datetime.now()
    test_list = [
        # input time, result time
        ('3:20:00 AM', '0:20'),
        ('15:30:00 PM', '12:30'),
        ('16:00:00 /', '13:00'),
        ('21:00:00', '18:00')
    ]

    strf_string = '%#H:%M' if platform.system() == 'Windows' else '%-H:%M'

    for time, result in test_list:
        if platform.system() == 'Windows':
            assert to_pacific_time(time, today).strftime(strf_string) == result


def test_to_pacific_time_newscasts():
    test_list = [
        # input time, result time
        ('3:20:00', '0:20'),
        ('15:30:00', '12:30'),
        ('16:00:00', '13:00'),
        ('21:00:00', '18:00')
    ]
    for time, result in test_list:
        assert to_pacific_time_newscasts(time) == result


def test_clean_header_list():
    sample_header_list = [
        parse('9/28/2020'),
        parse('9/29/2020'),
        'SOURCE'
    ]
    result = [
        datetime.datetime(2020, 9, 28),
        datetime.datetime(2020, 9, 29)
    ]
    assert clean_header_list(sample_header_list) == result
