"""
queue_parser.py
Parse through interconnection queue
Create CSVs of active, in-service, and withdrawn projects with cleaned county names and project type indicators
"""
import pandas as pd
import helpers as hp
from pathlib import Path
import state_names as sn
import re


def remove_spaces(cell):
    """
    Removes spaces from a pandas df cell
    :param cell:
    :return:
    """
    if not pd.isna(cell):
        cell = cell.replace(" ", "")
    return cell


def expand_state_name(cell):
    """
    Expand state name from NY->New York, MA->"Massachussets" using dict in state_names.py
    :param cell:
    :return:
    """
    if cell in sn.all_states.keys():
        cell = sn.all_states[cell]
    return cell


def set_status_indicator(f_name):
    indicator = 2
    if "service" in f_name:
        indicator = 1
    elif "withdrawn" in f_name:
        indicator = 0
    return indicator


def add_withdrawn_indicator(data_frame, indicator):
    if not data_frame.empty:
        data_frame = data_frame.copy()
        data_frame["Indicator"] = indicator  # 1 == in service, 0 == withdrawn
    else:
        print("Warning: attempting to add indicators to an empty data frame")
    return data_frame


def select_columns(projects, incl_developer, fuel_type):
    projects["State_full"] = projects["State"]
    projects["State"] = projects["State"].apply(expand_state_name)
    projects["State"] = projects["State"].apply(remove_spaces)
    projects_of_selected_fuel = projects.loc[projects['Type'] == fuel_type]
    columns = ['Position', 'Type', 'County', 'State_full', 'State', 'Indicator']
    if incl_developer:
        columns += 'Developer Name'
    return projects_of_selected_fuel[columns]


def try_to_select_columns(projects, incl_developer=False, fuel_type="W"):
    """
    Selects columns of interest and reformats from pandas df
    :param incl_developer:
    :param projects:
    :param fuel_type: project type (ex: "W")
    :return:
    """
    if not projects.empty:
        try:
            projects = select_columns(projects, incl_developer, fuel_type)
        except KeyError as k:
            print("ERR in select_columns():", k)
    return projects


def create_dataframe_save_name(file_name):
    name_components = file_name.split("-")
    region_name = name_components[0]
    project_type = name_components[-1].split(".")[0]
    save_name = region_name + "_" + project_type + ".csv"
    print("New name from {}\nto {}".format(file_name,save_name))
    return save_name


def name_and_save_dataframe(f_name, path, data_frame):
    """
    Creates .CSV of selected columns
    :param f_name: name of queue file to use in new .CSV name
    :param name_ext: "_active", "_in_service", or "_in_service"
    :param path: path to save .CSV file to
    :param data_frame: pandas dataframe to get data from
    :return: None
    """
    name_out = create_dataframe_save_name(f_name)
    hp.save_csv(name_out, data_frame, path)  # save CSV with results
    return


def remove_county(cell):
    """
    Removes " County" and punctuation from county name
    :param cell: cell containing the County or State name string
    :return: cell=cleaned cell string
    """
    if type(cell) is str:  # and len(cell) >0:
        cell = re.sub(r'[^\w\s]', '', cell)
        if " County" in cell:
            cell = cell.replace(" County", "")
    return cell


def create_csv(filename, path, incl_developer):
    """
    :param f_name: file name of .xlsx to create filtered .CSV of
    :param path: path to read .xlsx files from  (/training)
    and path to save .CSV files to (/training)
    :return: None
    """
    data_frame = hp.check_path_and_load_data(filename, path)
    indicator = set_status_indicator(filename)
    data_frame = add_withdrawn_indicator(data_frame, indicator)
    data_frame = try_to_select_columns(data_frame, incl_developer, fuel_type="W")  # only pass a single data_frame
    data_frame['County_clean'] = data_frame['County'].apply(remove_county)  # remove "County" from county names
    data_frame = data_frame.rename(columns={'County':'County_clean', 'County_clean':'County'})
    print(data_frame)
    if not data_frame.empty:
        name_and_save_dataframe(filename, path, data_frame)
    return


def main():
    path = "/Users/derekwacks/Documents/Interconnection/code/data/training"
    f_names = {
        "NYISO_xlsx_files": ["NYISO-Interconnection-Queue-active.xlsx",
                "NYISO-Interconnection-Queue-inservice.xlsx",
                "NYISO-Interconnection-Queue-withdrawn.xlsx",],
        "ISONE_xlsx_files": ["ISONE-Interconnection-Queue-active.xlsx",
                "ISONE-Interconnection-Queue-inservice.xlsx",
                "ISONE-Interconnection-Queue-withdrawn.xlsx",],
        "MISO_xlsx_files": ["MISO-Interconnection-Queue-active.xlsx",
                            "MISO-Interconnection-Queue-inservice.xlsx",
                            "MISO-Interconnection-Queue-withdrawn.xlsx",],
        "PJM_xlsx_files": ["PJM-Interconnection-Queue-active.xlsx",
                            "PJM-Interconnection-Queue-inservice.xlsx",
                            "PJM-Interconnection-Queue-withdrawn.xlsx",],
    }
    for iso in f_names.keys():
        for filename in f_names[iso]:
            create_csv(filename, path, incl_developer=False)
    return


if __name__ == "__main__":
    main()
