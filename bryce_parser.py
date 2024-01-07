"""
bryce_parser.py
Parse and process data from Robert Bryce database of opposed wind projects
"""

import helpers as hp
import pandas as pd
import numpy as np
import state_names as sn


def get_county(cell, ver):
    name = np.NaN
    if "County" in cell:
        cell = cell.split(" ")
        for i in range(len(cell)):
            if cell[i] == "County" and (i-1) < len(cell) and i >= 1:
                if ver == 1:
                    name = " ".join(cell[:i])
                elif ver == 2:
                    name = cell[i-1]
    print("Setting", name)
    return name

def update_state(cell):
    return sn.all_states[cell]


def find_county_name(f_name, path_to_data):
    """
    Find county name from "Entity" and "Government" columns in excel sheet of opposed projects
    :param f_name: name of Bryce starting database
    :param path_to_data: path to location of file
    :return: None
    """
    data = hp.check_path_and_load_data(f_name, path_to_data)
    # If Entity column contains "Township", find county in Government column
    temp = data[data['Entity'].str.contains("Township")]
    data['County'] = temp['Government'].apply(get_county, ver=2)
    # Else, find county in Entity column
    temp = data[data['County'].isnull()]
    data['County'] = temp['Entity'].apply(get_county, ver=1)
    data['State'] = data['State'].apply(update_state)
    # Don't rerun
    #hp.save_csv("opposed_projects_partially_filled.csv", data, path_to_data)
    return

def main():
    f_name = "opposed_projects_bryce.xlsx"
    path_to_data = "/Users/derekwacks/Documents/Interconnection/code/data/"
    find_county_name(f_name, path_to_data)


if __name__ == "__main__":
    main()

