import pandas as pd


sheet_ingest = {
    # Sheet name
    'ME-WE Cut IDs': [
        # cut id, cut number pairs
        ('ME Cut IDs', 'Unnamed: 1'),
        ('Unnamed: 3', 'Unnamed: 4'),
        ('Unnamed: 6', 'Unnamed: 7'),
        ('Unnamed: 9', 'Unnamed: 10')
    ],
    'ATC-WATC Cut IDs': [
        ('ATC Cut IDs', 'Unnamed: 1'),
        ('Unnamed: 3', 'Unnamed: 4'),
        ('Unnamed: 6', 'Unnamed: 7')
    ]
}


def get_id_cut_number_converter(input_file):
    """ This module returns a dictionary in which takes
    a cut ID (for Morning Edition, Weekend Edition, ATC, etc.) as
    a key and returns the actual cut number
    """
    pd_file = pd.ExcelFile(input_file)

    converter_dict = {}
    for sheet, row_pairs in sheet_ingest.items():
        df = pd.read_excel(input_file, sheet)
        converter_dict.update(process_one_dataframe(df, row_pairs))

    return converter_dict


def process_one_dataframe(df, row_pair_tuples: list):

    output_dict = {}
    for each_pair in row_pair_tuples:
        output_dict.update(process_columns(df, *each_pair))
    return output_dict


def process_columns(dataframe, cut_id_column: str, cut_number_column: str) -> dict:
    one_set = dataframe[[cut_id_column, cut_number_column]]
    one_set = one_set.dropna(0)
    one_set = one_set.to_dict(orient='list')

    return {
        seg_code: str(int(cut_no))
        for seg_code, cut_no in zip(
            one_set.get(cut_id_column),
            one_set.get(cut_number_column)
        )
    }


"""
Sample Return for get_id_cut_number_converter

{
    'ME01': '64664', 'ME02': '64665', 'ME03': '64666', 'ME04': '64667', 'ME05': '64668', 'ME06': '64669', 'ME07': '64670', 
    'ME08': '64671', 'ME09': '64672', 'ME10': '64673', 'ME11': '64674', 'ME12': '64675', 'ME13': '64676', 'ME14': '64685', 
    'ME15': '64686', 'ME16': '64687', 'ME17': '64688', 'ME18': '64689', 'ME19': '64690', 'ME20': '64691', 'WE01': '64642', 'WE02': '64648', 
    'WE03': '64649', 'WE04': '64650', 'WE05': '64651', 'WE06': '64652', 'ME21': '64692', 'ME22': '64693', 'ME23': '64694', 'ME24': '64695', 
    'ME25': '64696', 'ME26': '64697', 'ME27': '64698', 'ME28': '64699', 'ME29': '64700', 'ME30': '64701', 'WE07': '64653', 
    'WE08': '64654', 'WE09': '64655', 'WE10': '64656', 'WE11': '64657', 'WE12': '64663', 'ME31': '64702', 'ME32': '64703', 'ME33': '64704', 
    'ME34': '64705', 'ME35': '64706', 'ME36': '64707', 'ME37': '64708', 'ME38': '64709', 'ME39': '64710', 'ME40': '64711', 'ME41': '64712', 
    'ME42': '64713', 'ME43': '64714', 'ME44': '64715', 'ME45': '64716', 'ME46': '64717', 'ME47': '64718', 'ME48': '64724', 'ME49': '64725', 
    'ME50': '64726', 'ME51': '64727', 'ME52': '64728', 'ME53': '64737', 'ME54': '64738', 'ME55': '64739', 'ATC01': '64740', 'ATC02': '64741', 
    'ATC03': '64742', 'ATC04': '64743', 'ATC05': '64744', 'ATC06': '64745', 'ATC07': '64746', 'ATC08': '64747', 'ATC09': '64748', 'ATC10': '64749', 
    'WA01': '64770', 'WA02': '64771', 'WA03': '64772', 'WA04': '64773', 'WA05': '64774', 'WA06': '64775', 'ATC11': '64750', 'ATC12': '64751', 
    'ATC13': '64752', 'ATC14': '64753', 'ATC15': '64754', 'ATC16': '64755', 'ATC17': '64756', 'ATC18': '64757', 'ATC19': '64758', 'ATC20': '64759', 
    'ATC21': '64760', 'ATC22': '64761', 'ATC23': '64762', 'ATC24': '64763', 'ATC25': '64764', 'ATC26': '64765', 'ATC27': '64766', 'ATC28': '64767', 
    'ATC29': '64768', 'ATC30': '64769'
}
"""