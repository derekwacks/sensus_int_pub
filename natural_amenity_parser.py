"""
natural_amenity_parser.py
Only need to run this once to create natural amenities CSV file
"""
import numpy as np
import pandas as pd
import json
from pathlib import Path
import re
import helpers as hp
import state_names as sn


def load_json(f_name):
    """
    "/Natural-Amenities-by-US-County.json"
    Didn't work very well; an attempt to parse the amenity data in json format
    :return:
    """
    path_to_data = "/Users/derekwacks/Documents/Interconnection/code/data"
    data_path = path_to_data + f_name
    file_check = Path(data_path)
    if file_check.exists():
        with open(data_path, 'r', encoding='utf-8') as f:
            amenities_data = json.load(f)
            return amenities_data
    else:
        print("{} not found".format(f_name))
    return None


def reformat_json(df):
    pass


def add_space(state):
    """
    Checks if the state should have two subwords (ie "New York", "New Jersey", NOT "Vermont")
    Uses state_names.py as a lookup dictionary
    :param state: str state name without a space (ie "NewYork", "Vermont")
    :return: state name with a space, if it normally has one (ie "New York")
    """
    if state in sn.double_states.keys():
        return sn.double_states[state]
    else:
        return state


def reformat(cell, item="County", include_county=True):
    """
    Reformats and cleans a County or State name string
    :param cell: cell containing the County or State name string
    :param item: type ("County", or another string)
    If we want to change how spaces are dealt with, can use the item="State" flag
    :param include_county: bool to determine if the string "County" is included
    :return: cell=cleaned cell string
    """
    cell = cell[7:-1]
    cell = re.sub(r'[^\w\s]', '', cell)
    cell = cell.split(" ")[1:-1]
    if len(cell) > 0:
        try:
            if include_county:
                cell[0] = cell[0].replace("County", " County")
            else:
                cell[0] = cell[0].replace("County", "")
            if item == "County":
                cell = cell[0]
            else:
                cell = cell[1]
        except:
            print("Couldn't add space: \"County\" not found in ", cell)
    return cell


def apply_to_df(df):
    """
    Driving function to apply reformat to County and State names
    Renames dataframe columns
    :param df: pandas dataframe to clean data and rename columns of
    :return: amenities=cleaned and reformatted dataframe
    """
    df['County_clean'] = df['County'].apply(reformat, item="County", include_county=False)
    df['State_clean'] = df['County'].apply(reformat, item="State", include_county=False)
    amenities = df[['State', 'County', 'County_clean', 'State_clean', 'NaturalAmenityTier', 'NaturalAmenityRank']]
    names = {'County': 'County_clean', 'County_clean': 'County', 'State': 'State_clean', 'State_clean': 'State'}
    amenities = amenities.rename(columns=names)
    return amenities


def main():
    path_to_data = "/Users/derekwacks/Documents/Interconnection/code/data/"
    f_name = "Natural-Amenities-by-US-County.csv"
    df = hp.check_path_and_load_data(f_name, path_to_data)
    amenities = apply_to_df(df)
    name = "Natural_Amenities_by_County_cleaned.csv"
    hp.save_csv(name, amenities, path_to_data)
    return


if __name__ == "__main__":
    main()

