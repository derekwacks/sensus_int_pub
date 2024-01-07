"""
geojson_creator.py
Creates geojson file for Mapbox using towns in the interconnection queue
~ * ~ * ~ * ~ *
parse .csv of data
for each line of data, create geojson formatted file
save file
"""
import pandas as pd
from pathlib import Path
import json
import helpers as hp


def create_feature(row):
    """
    Creates geojson feature row for feature collection
    :param row: dictionary of project data
    :return: ret=formatted feature json
    """
    coordinates = row['Locations'][1:-1]
    coors = coordinates.split(", ")
    coors = [float(i) for i in coors]
    ret = {
        "type": "Feature",
        "properties": {
            "title": row['Project Name'],
            "description": "stuff!",
            "County": row['County'],
            "State": row['State'],
            "DeveloperName": str(row['Developer Name']),
            "PointsofInterconnection": str(row['Points of Interconnection']),
        },
        "geometry":{
            "coordinates": coors,
            "type": "Point"
        }
    }
    return ret

def add_geojsons(full_d_frame):
    """
    Driver for create_feature() function to apply to pandas dataframe
    :param full_d_frame: pandas dataframe to operate on
    :return: full_d_frame=updated dataframe
    """
    full_d_frame['geojsons'] = full_d_frame.apply(create_feature, axis=1)
    return full_d_frame

def create_full_geojson(full_d_frame):
    """
    Writes geojson features from pandas dataframe to .geojson file
    :param full_d_frame: dataframe to pull collection of features from
    :return: None
    """
    gj = list(full_d_frame['geojsons'])
    geojson = {
        "features": gj,
        "type": "FeatureCollection"
    }
    with open('data/interconnection.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    print("Done creating interconnection.geojson")


def main():
    path_to_data = "/Users/derekwacks/Documents/Interconnection/code/data/"
    f_name = "locs.csv"
    full_d_frame = hp.load_csv(f_name, path_to_data)
    print(full_d_frame)
    full_d_frame = add_geojsons(full_d_frame)
    create_full_geojson(full_d_frame)
    return

if __name__ == "__main__":
    main()

