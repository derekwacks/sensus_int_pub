"""
data_merger.py
helper functions to read from cleaned CSV's and merge data from different queues together
"""
import pandas as pd
import helpers as hp
import numpy as np
from pathlib import Path


def add_amenity_data_and_save(f_name, path):
    """
    Merge queue data stored at f_name with county amenity tier data
    Create and save a new .CSV
    :param f_name: name of queue data file
    :param path: path to queue data, and where to save new .CSV to
    :return: name of new merged CSV file
    """
    f_data = hp.check_path_and_load_data(f_name, path)
    merged_df = f_data.copy()
    path_to_data = Path(path, "../")

    amenities_f = "Natural_Amenities_by_County_cleaned.csv"
    amenities_data = hp.check_path_and_load_data(amenities_f, path_to_data)
    merged_df = merged_df.merge(amenities_data, how="left", on=["County", "State"])

    # TODO: add other data here!
    #opposed_projects_f = "opposed_projects_filled.csv"
    #opposed_projects = hp.check_path_and_load_data(opposed_projects_f, path_to_data)
    #merged_df = merged_df.merge(opposed_projects, how="left", on=["County", "State"])

    save_as = "merged_" + f_name
    hp.save_csv(save_as, merged_df, path)
    return


def add_amenity_data_driver(f_names, path):
    """
    Adds amenity indices to each row in each csv included in f_names
    :param f_names: list of CSV file names (ex: "NYISO_withdrawn.csv", "NYISO_inservice.csv", etc.)
    :param path: path to csv files
    :return: list of new file names  (ex: "merged_NYISO_withdrawn.csv", "merged_NYISO_inservice.csv", etc.)
    """
    save_names = []
    for n in f_names:
        save_name = "merged_" + n
        add_amenity_data_and_save(n, path)
        save_names.append(save_name)
    return save_names


def add_indicators(saved_names):
    all_data = []
    for n in saved_names:
        indicator = 3
        if "service" in n:
            indicator = 1
        elif "withdrawn" in n:
            indicator = 0
        all_data.append((n, indicator))
    return all_data


def create_matrix(f_names_indic_tuples, path, cols_to_include):
    """
    Assemble a data frame with in-service (successfully operating) and withdrawn projects and amenity tiers
    :param f_names_indic_tuples: list of .CSV data files
    :param path: path to files
    :return: pandas dataframe with in-service indicator (0 or 1) and amenity tier
    """
    merged = pd.DataFrame()
    for tup in f_names_indic_tuples:
        name = tup[0]
        indicator = tup[1]
        data = hp.check_path_and_load_data(name, path)
        if not data.empty:
            data = data[cols_to_include].copy()
            data = data[data['NaturalAmenityTier'].notnull()]  # remove Nan values
            if 'Opposed' in cols_to_include:
                data['Opposed'] = data['Opposed'].fillna(0)
            data['indicator'] = indicator  # 1 == in service, 0 == withdrawn
            merged = pd.concat([merged, data])
    return merged

