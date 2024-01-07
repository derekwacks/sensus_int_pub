"""
helpers.py
Helper functions (mainly regarding CSV operations)
"""
import pandas as pd
from pathlib import Path


def find_type(f_name):
    """
    :param f_name: data file name
    :return: ".CSV" or ".XSLX"
    """
    ending = f_name.split(".")[-1]
    return ending


def save_csv(name, d_frame, path):
    """
    :param name: new file name to save as
    :param d_frame: data frame to write to csv
    :param path: path to folder location
    :return: None
    """
    full_path = Path(path, name)
    d_frame.to_csv(full_path)
    return


def create_dataframe_from_file(f_name, full_path, sheet_name):
    f_type = find_type(f_name)
    if f_type == "csv":
        d_frame = pd.read_csv(full_path)
    elif f_type == "xlsx":
        d_frame = pd.read_excel(full_path, sheet_name=sheet_name)
        if sheet_name != 0:
            k = next(iter(d_frame))  # same as next(iter(d.keys())), get first key in dict
            d_frame = d_frame[k]
            if len(d_frame.keys()) > 1:  # if isinstance(data_frame, dict)
                print("WARNING: returning {} but more data frames are available from this .xlsx".format(k))
    else:
        d_frame = pd.DataFrame()
    return d_frame


def check_path_and_load_data(f_name, path_to_data):
    """
    Loads data file into pandas DF
    :param f_name: name of data file
    :param path_to_data: path to data file
    :return: d_frame=data frame d_frame from pandas
    """
    sheet_name = 0  # sheet_name=None to get all sheets
    full_path = Path(path_to_data, f_name)
    print("Loading:", full_path)
    if full_path.exists():
        d_frame = create_dataframe_from_file(f_name, full_path, sheet_name)
        return d_frame
    else:
        print("Error: {} not found".format(f_name))
        return pd.DataFrame()

