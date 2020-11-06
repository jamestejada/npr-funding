import pytz
import pandas as pd
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from modules.processing.cut_converter import get_id_cut_number_converter
from modules.config.settings import NEWS_FILE


regular_funding_credits = [
    '4:45',
    '5:21', '5:34', '5:45',
    '6:21', '6:34', '6:45',
    '7:21', '7:34', '7:45',
    '8:21', '8:34', '8:45',
    '15:35', '15:58',
    '16:20', '16:35', '16:58',
    '17:20', '17:35', '17:58',
    '18:20'
]

newscast_funding_credits = [
    '5:05', '6:05', '7:05',
    '8:05', '9:05', '14:05', 
    '15:05', '16:05', '17:05', '18:05'
]

full_sorted_list = [
    '4:45',
    '5:05', '5:21', '5:34', '5:45',
    '6:05', '6:21', '6:34', '6:45',
    '7:05', '7:21', '7:34', '7:45',
    '8:05', '8:21', '8:34', '8:45',
    '9:05', '14:05', 
    '15:05', '15:35', '15:58',
    '16:05', '16:20', '16:35', '16:58',
    '17:05', '17:20', '17:35', '17:58',
    '18:05', '18:20'
]

cut_id_converter = get_id_cut_number_converter(NEWS_FILE)


# main
def get_time_to_cutid_converter(input_file_news, input_file_newscasts):

    out_dict = {}
    out_dict['NC'] = get_newscast_dict(input_file_newscasts)

    for show in ['ME', 'ATC']:
        out_dict[show] = get_show_dict(show, input_file_news)

    # merge all three sub-dictionaries in out_dict
    dict_for_dataframe = merge_show_dicts(out_dict)

    return sort_output_dict(dict_for_dataframe)


def get_show_dict(show, input_file_news):
    df = pd.read_excel(input_file_news, f'{show} Sched', header=3)
    header_list = clean_header_list(df.columns.to_list())
    sample_key_for_source = date_to_string(header_list[2])
    out_dict = {}

    for each_day in header_list:
        raw_day_dict = get_one_day_dict(each_day, df, show)
        converted_day_dict = time_convert_whole_day(raw_day_dict, each_day)

        if converted_day_dict:
            each_day_str = date_to_string(each_day)
            out_dict[each_day_str] = converted_day_dict
    out_dict['SOURCE'] = {time: show for time in out_dict.get(sample_key_for_source)}
    
    return out_dict


def merge_show_dicts(meta_dict):
    out_dict = {}
    for show, show_dict in meta_dict.items():
        for day, day_dict in show_dict.items():
            try:
                out_dict[day].update(day_dict)
            except KeyError:
                out_dict[day] = day_dict
    return out_dict


def sort_output_dict(input_dict):
    output_dict = {}
    for day, day_dict in input_dict.items():
        # not working somewhere here.
        output_dict[day] = {time: day_dict.get(time) for time in full_sorted_list}
    
    return output_dict


def date_to_string(datetime_obj):
    try:
        return datetime_obj.strftime('%d-%b')
    except (ParserError, AttributeError):
        return None


def clean_header_list(raw_header_list: list) -> list:
    # raw_header_list is df.columns.to_list()
    output_list = []
    for header in raw_header_list:
        header_parse = date_to_string(header)
        if header_parse is not None:
            output_list.append(header)
    return output_list


def time_convert_whole_day(sched_dict, datetime_header, time_coumn_header='Times (ET)'):
    out_dict = {}
    for times_et, cut_id in zip(sched_dict.get(time_coumn_header), sched_dict.get(datetime_header)):
        # converted_pacific_str = to_pacific_time(times_et, datetime_header).strftime('%-H:%M') # Linux
        converted_pacific_str = to_pacific_time(times_et, datetime_header).strftime('%#H:%M')
        if converted_pacific_str in regular_funding_credits:
            out_dict[converted_pacific_str] = convert_cut_id_to_cut_number(cut_id)
    return out_dict


def convert_cut_id_to_cut_number(cut_id):
    return int(cut_id_converter.get(cut_id))


def get_one_day_dict(datetime_obj, dataframe, show, time_header='Times (ET)') -> dict:

    one_day = dataframe[[time_header, datetime_obj]]
    one_day = one_day.dropna(0)
    result_df = one_day[one_day[datetime_obj].str.match(f'^{show}.*')]
    return result_df.to_dict(orient='list')


PACIFIC_TIMEZONE = pytz.timezone('US/Pacific')
EASTERN_TIMEZONE = pytz.timezone('US/Eastern')


def to_pacific_time(
            eastern_time: str,
            one_day_dt: object,
            ignore_chars=['/', 'PM', 'AM']
            ) -> object:
    """ returns a converted pacific timezone datetime object
    from a datetime representing a day and an eastern time string
    from the NPR reference spreadsheet.
    """

    # remove unwanted characters from eastern_datetime
    for character in ignore_chars:
        eastern_time = eastern_time.replace(character, '')

    eastern_datetime = parse(eastern_time)
    converted_eastern_datetime = one_day_dt.replace(
        hour=eastern_datetime.hour,
        minute=eastern_datetime.minute
        )

    # convert eastern to pacific time
    return EASTERN_TIMEZONE.localize(
        converted_eastern_datetime, is_dst=None
    ).astimezone(PACIFIC_TIMEZONE)


def get_newscast_dict(newscast_file):

    time_header = 'AM Newscasts'
    df = pd.read_excel(newscast_file, 'Page 3', header=1, dtype={time_header: str})

    header_list = [
        date_to_string(header) if not header == time_header else header 
        for header in df.columns.to_list()
        ]


    df[time_header] = df[df[time_header].str.len() == 8]
    df = df.dropna()
    df[time_header] = pd.to_datetime(df[time_header]).dt.strftime('%H:%M')
    raw_time_list = df[time_header].to_list()
    time_list = list(map(to_pacific_time_newscasts, raw_time_list))
    df[time_header] = time_list
    df = df.set_index(time_header)
    # Add Source column
    df['SOURCE'] = ['NC' for i in range(len(df.index))]

    df_dict = df.to_dict()

    return clean_newscast_dict(df_dict)


def clean_newscast_dict(raw_dict):
    output_dict = {}
    keys = list(raw_dict.keys())
    desired_keys = [*keys[:5], keys[7]]

    for day, day_dict in raw_dict.items():
        if day not in desired_keys:
            continue
        day_string = date_to_string(day) if type(day) is not str else day
        output_dict[day_string] = {}
        for time in day_dict:
            if time in newscast_funding_credits:
                output_dict[day_string].update({time: day_dict[time]})

    return output_dict


def to_pacific_time_newscasts(eastern_time):
    converted_eastern_datetime = parse(eastern_time)

    # convert eastern to pacific time
    return EASTERN_TIMEZONE.localize(
            converted_eastern_datetime, is_dst=None
        # ).astimezone(PACIFIC_TIMEZONE).strftime('%-H:%M') # LInux version
        ).astimezone(PACIFIC_TIMEZONE).strftime('%#H:%M')

"""
Sample Output for get_time_to_cutid_converter

{
    '28-Sep': {
        '4:45': 64669, 
        '5:05': 64964, 
        '5:21': 64670, 
        '5:34': 64671, 
        '5:45': 64713, 
        '6:05': 64965, 
        '6:21': 64664, 
        '6:34': 64665, 
        '6:45': 64666, 
        '7:05': 65000, 
        '7:21': 64667, 
        '7:34': 64668, 
        '7:45': 64669, 
        '8:05': 64964, 
        '8:21': 64670, 
        '8:34': 64671, 
        '8:45': 64714, 
        '9:05': 64988, 
        '14:05': 64964, 
        '15:05': 65040, 
        '15:35': 64741, 
        '15:58': 64742, 
        '16:05': 65004, 
        '16:20': 64743, 
        '16:35': 64744, 
        '16:58': 64745, 
        '17:05': 64964, 
        '17:20': 64740, 
        '17:35': 64741, 
        '17:58': 64742, 
        '18:05': 65040, 
        '18:20': 64743
        }, 
    '29-Sep': {
        
        '4:45': 64685, 
        '5:05': 64964, 
        '5:21': 64686, 
        '5:34': 64687, 
        '5:45': 64716, 
        '6:05': 64964, 
        '6:21': 64672, 
        '6:34': 64673, 
        '6:45': 64674, 
        '7:05': 64999, 
        '7:21': 64675, 
        '7:34': 64676, 
        '7:45': 64685, 
        '8:05': 64964, 
        '8:21': 64686, 
        '8:34': 64687, 
        '8:45': 64717, 
        '9:05': 64895, 
        '14:05': 64965, 
        '15:05': 65044, 
        '15:35': 64747, 
        '15:58': 64748, 
        '16:05': 64964, 
        '16:20': 64749, 
        '16:35': 64750, 
        '16:58': 64751, 
        '17:05': 64965, 
        '17:20': 64746, 
        '17:35': 64747, 
        '17:58': 64748, 
        '18:05': 65044, 
        '18:20': 64749
        }, 
    '30-Sep': {
        '4:45': 64693, 
        '5:05': 64973, 
        '5:21': 64694, 
        '5:34': 64695, 
        '5:45': 64724, 
        '6:05': 64964, 
        '6:21': 64688, 
        '6:34': 64689, 
        '6:45': 64690, 
        '7:05': 64965, 
        '7:21': 64691, 
        '7:34': 64692, 
        '7:45': 64693, 
        '8:05': 64973, 
        '8:21': 64694, 
        '8:34': 64695, 
        '8:45': 64725, 
        '9:05': 65049, 
        '14:05': 64965, 
        '15:05': 65045, 
        '15:35': 64753, 
        '15:58': 64754, 
        '16:05': 64964, 
        '16:20': 64755, 
        '16:35': 64756, 
        '16:58': 64757, 
        '17:05': 64965, 
        '17:20': 64752, 
        '17:35': 64753, 
        '17:58': 64754, 
        '18:05': 65045, 
        '18:20': 64755
        }, 
    '01-Oct': {
        '4:45': 64701, 
        '5:05': 64999, 
        '5:21': 64702, 
        '5:34': 64703, 
        '5:45': 64727, 
        '6:05': 64973, 
        '6:21': 64696, 
        '6:34': 64697, 
        '6:45': 64698, 
        '7:05': 65000, 
        '7:21': 64699, 
        '7:34': 64700, 
        '7:45': 64701, 
        '8:05': 64999, 
        '8:21': 64702, 
        '8:34': 64703, 
        '8:45': 64728, 
        '9:05': 64970, 
        '14:05': 64972, 
        '15:05': 65052, 
        '15:35': 64759, 
        '15:58': 64760, 
        '16:05': 65004, 
        '16:20': 64761, 
        '16:35': 64762, 
        '16:58': 64763, 
        '17:05': 64972, 
        '17:20': 64758, 
        '17:35': 64759, 
        '17:58': 64760, 
        '18:05': 65052, 
        '18:20': 64761
        }, 
    '02-Oct': {
        '4:45': 64709, 
        '5:05': 65000, 
        '5:21': 64710, 
        '5:34': 64711, 
        '5:45': 64738, 
        '6:05': 64973, 
        '6:21': 64704, 
        '6:34': 64705, 
        '6:45': 64706, 
        '7:05': 64999, 
        '7:21': 64707, 
        '7:34': 64708, 
        '7:45': 64709, 
        '8:05': 65000, 
        '8:21': 64710, 
        '8:34': 64711, 
        '8:45': 64739, 
        '9:05': 64895, 
        '14:05': 65004, 
        '15:05': 65040, 
        '15:35': 64765, 
        '15:58': 64766, 
        '16:05': 64973, 
        '16:20': 64767, 
        '16:35': 64768, 
        '16:58': 64769, 
        '17:05': 65004, 
        '17:20': 64764, 
        '17:35': 64765, 
        '17:58': 64766, 
        '18:05': 65040, 
        '18:20': 64767
        }, 
    'SOURCE': {
        '4:45': 'ME', 
        '5:05': 'NC', 
        '5:21': 'ME', 
        '5:34': 'ME', 
        '5:45': 'ME', 
        '6:05': 'NC', 
        '6:21': 'ME', 
        '6:34': 'ME', 
        '6:45': 'ME', 
        '7:05': 'NC', 
        '7:21': 'ME', 
        '7:34': 'ME', 
        '7:45': 'ME', 
        '8:05': 'NC', 
        '8:21': 'ME', 
        '8:34': 'ME', 
        '8:45': 'ME', 
        '9:05': 'NC', 
        '14:05': 'NC', 
        '15:05': 'NC', 
        '15:35': 'ATC', 
        '15:58': 'ATC', 
        '16:05': 'NC', 
        '16:20': 'ATC', 
        '16:35': 'ATC', 
        '16:58': 'ATC', 
        '17:05': 'NC', 
        '17:20': 'ATC', 
        '17:35': 'ATC', 
        '17:58': 'ATC', 
        '18:05': 'NC', 
        '18:20': 'ATC'
        }
}

"""