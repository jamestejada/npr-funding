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
    a cut ID (for Morning Edition and Weekend Edition) as
    a key and returns the actual cut number
    """
    pd_file = pd.ExcelFile(input_file)

    converter_dict = {}
    for sheet, row_pairs in sheet_ingest.items():
        df = pd.read_excel(input_file, sheet)
        for each_pair in row_pairs:
            converter_dict.update(process_columns(df, *each_pair))

    return converter_dict


def process_columns(dataframe, cut_id_column, cut_number_column):
    one_set = dataframe[[cut_id_column, cut_number_column]]
    one_set = one_set.dropna(0)
    one_set = one_set.to_dict(orient='list')

    out_dict = {}
    for seg_code, cut_no in zip(
                            one_set.get(cut_id_column),
                            one_set.get(cut_number_column)
                            ):
        out_dict[seg_code] = str(int(cut_no))
    return out_dict
