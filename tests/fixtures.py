import pytest
import pandas as pd
from pathlib import Path
from modules.processing.cut_converter import sheet_ingest
from modules.processing.funding_credit_schedule import get_id_cut_number_converter


@pytest.fixture
def news_file():
    return Path.cwd().joinpath('tests', 'data', 'news.xls')


@pytest.fixture
def newscast_file():
    return Path.cwd().joinpath('tests', 'data', 'newscast.xls')


@pytest.fixture
def full_target_data(news_file):
    pd_file = pd.ExcelFile(news_file)

    converter_dict = {}
    new_sheet_ingest = sheet_ingest
    for sheet, row_pairs in new_sheet_ingest.items():
        df = pd.read_excel(news_file, sheet)
        for cut_id_column, cut_number_column in row_pairs:
            one_set = df[[cut_id_column, cut_number_column]]
            one_set = one_set.dropna(0)
            one_set.to_dict(orient='list')

            new_dict = {}
            for seg_code, cut_no in zip(one_set.get(cut_id_column), one_set.get(cut_number_column)):
                new_dict[seg_code] = str(int(cut_no))

            converter_dict.update(new_dict)
    
    return converter_dict


@pytest.fixture
def cut_id_converter(news_file):
    return get_id_cut_number_converter(news_file)


@pytest.fixture
def time_to_cutid_converter():
    return {'28-Sep': {'4:45': 64669, '5:05': 64964, '5:21': 64670, '5:34': 64671, '5:45': 64713, '6:05': 64965, '6:21': 64664, '6:34': 64665, '6:45': 64666, '7:05': 65000, '7:21': 64667, '7:34': 64668, '7:45': 64669, '8:05': 64964, '8:21': 64670, '8:34': 64671, '8:45': 64714, '9:05': 64988, '14:05': 64964, '15:05': 65040, '15:35': 64741, '15:58': 64742, '16:05': 65004, '16:20': 64743, '16:35': 64744, '16:58': 64745, '17:05': 64964, '17:20': 64740, '17:35': 64741, '17:58': 64742, '18:05': 65040, '18:20': 64743}, '29-Sep': {'4:45': 64685, '5:05': 64964, '5:21': 64686, '5:34': 64687, '5:45': 64716, '6:05': 64964, '6:21': 64672, '6:34': 64673, '6:45': 64674, '7:05': 64999, '7:21': 64675, '7:34': 64676, '7:45': 64685, '8:05': 64964, '8:21': 64686, '8:34': 64687, '8:45': 64717, '9:05': 64895, '14:05': 64965, '15:05': 65044, '15:35': 64747, '15:58': 64748, '16:05': 64964, '16:20': 64749, '16:35': 64750, '16:58': 64751, '17:05': 64965, '17:20': 64746, '17:35': 64747, '17:58': 64748, '18:05': 65044, '18:20': 64749}, '30-Sep': {'4:45': 64693, '5:05': 64973, '5:21': 64694, '5:34': 64695, '5:45': 64724, '6:05': 64964, 
'6:21': 64688, '6:34': 64689, '6:45': 64690, '7:05': 64965, '7:21': 64691, '7:34': 64692, '7:45': 64693, '8:05': 64973, '8:21': 64694, '8:34': 64695, '8:45': 64725, '9:05': 65049, '14:05': 64965, '15:05': 65045, '15:35': 64753, '15:58': 64754, '16:05': 64964, '16:20': 64755, '16:35': 64756, '16:58': 64757, '17:05': 64965, '17:20': 64752, '17:35': 64753, '17:58': 64754, '18:05': 65045, '18:20': 64755}, '01-Oct': {'4:45': 64701, '5:05': 64999, '5:21': 64702, '5:34': 64703, '5:45': 64727, '6:05': 64973, '6:21': 64696, '6:34': 64697, '6:45': 64698, '7:05': 65000, '7:21': 64699, '7:34': 64700, '7:45': 64701, '8:05': 64999, '8:21': 64702, '8:34': 64703, '8:45': 64728, '9:05': 64970, '14:05': 64972, '15:05': 65052, '15:35': 64759, '15:58': 64760, '16:05': 65004, '16:20': 64761, '16:35': 64762, '16:58': 64763, '17:05': 64972, '17:20': 64758, '17:35': 64759, '17:58': 64760, '18:05': 65052, '18:20': 64761}, '02-Oct': {'4:45': 64709, '5:05': 65000, '5:21': 64710, '5:34': 64711, '5:45': 64738, '6:05': 64973, '6:21': 64704, '6:34': 64705, '6:45': 64706, '7:05': 64999, '7:21': 64707, '7:34': 64708, '7:45': 64709, '8:05': 
65000, '8:21': 64710, '8:34': 64711, '8:45': 64739, '9:05': 64895, '14:05': 65004, '15:05': 65040, '15:35': 64765, '15:58': 64766, '16:05': 64973, '16:20': 64767, '16:35': 64768, '16:58': 64769, '17:05': 65004, '17:20': 64764, '17:35': 64765, '17:58': 64766, '18:05': 65040, '18:20': 64767}, 'SOURCE': {'4:45': 'ME', '5:05': 'NC', '5:21': 'ME', '5:34': 'ME', '5:45': 'ME', '6:05': 'NC', '6:21': 'ME', '6:34': 'ME', '6:45': 'ME', '7:05': 'NC', '7:21': 'ME', '7:34': 'ME', '7:45': 'ME', '8:05': 'NC', '8:21': 'ME', '8:34': 'ME', '8:45': 'ME', '9:05': 'NC', '14:05': 'NC', '15:05': 'NC', '15:35': 'ATC', '15:58': 'ATC', '16:05': 'NC', '16:20': 'ATC', '16:35': 'ATC', '16:58': 'ATC', '17:05': 'NC', '17:20': 'ATC', '17:35': 'ATC', '17:58': 'ATC', '18:05': 'NC', '18:20': 'ATC'}}