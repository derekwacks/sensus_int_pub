"""
coordinate_locator.py

Finds coordinates for towns in the interconnection queue
~ * ~ * ~ * ~ *
parse .csv of data
for each line of data, find coordinates using Nominatim
save data in new dataframe
save file
"""
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd
from pathlib import Path
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from datetime import datetime
import helpers as hp

def geo(place, mapbox_orientation=True):
    """
    Call geopy geocoder API to get coordinates
    :param place: string name of county (or address more generally) to lookup
    :param mapbox_orientation: bool to flip longitude and latitude (Mapbox stores these backwards as lat,long)
    :return: list [long, lat] or [lat, long] or None
    """
    name = datetime.now().strftime('mygeo_%H-%M-%S')
    geolocator = Nominatim(user_agent=name)
    try:
        location = geolocator.geocode(place)
        if mapbox_orientation:
            return [location.longitude, location.latitude]
        else:
            return [location.latitude, location.longitude]
    except:
        return None

def clean_counties(counties):
    """
    Remove "County" from any county names
    :param d_frame:
    :return:
    """
    #d_frame['County'] = d_frame['County'].apply(geo)
    return counties

def find_coordinates(d_frame):
    """
    Driver function to find coordinates for locations in "Merged" column of pandas dataframe d_frame
    Store coordinates [long, lat] in pandas dataframe d_frame at "Locations"
    :param d_frame: pandas dataframe to pull County and State strings from, and save coordinates to
    :return: d_frame=updated pandas dataframe
    """
    d_frame['Merged'] = d_frame['County'] + ", " + d_frame['State']
    d_frame['Locations'] = d_frame['Merged'].apply(geo)
    return d_frame

def find_coordinates2(d_frame):
    """
    (Not using)
    Alternative geolocator API strategy to get around timeout
    :param d_frame: pandas dataframe to pull County and State strings from, and save coordinates to
    :return: d_frame=updated pandas dataframe
    """
    geolocator = Nominatim(user_agent="sensus")
    #geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.0001)
    d_frame['Merged'] = d_frame['County'] + ", " + d_frame['State']
    d_frame['Locations'] = d_frame['Merged'].apply(geolocator.geocode)
    return d_frame

def geo_tester():
    """
    Finds the location of a single string place using geocode()
    :return: None
    """
    place = "Ball Hill Wind"  # "Genesee, NY"
    geolocator = Nominatim(user_agent="Tester")
    location = geolocator.geocode(place)
    print(location)
    print(location.latitude, location.longitude)
    return

def main():
    path_to_data = "/Users/derekwacks/Documents/Interconnection/code/data/"
    loc_path = path_to_data + "locs.csv"
    loc_file = Path(loc_path)
    if loc_file.exists() == False:
        f_name = "NYISO_InterconnectionQueue_locations.csv"
        d_frame = hp.load_csv(f_name, path_to_data)
        d_frame['County'] = d_frame['County'].apply(clean_counties)  # Clean
        start_time_1 = datetime.now()
        full_d_frame = find_coordinates(d_frame)
        print("Time elapsed:", datetime.now()-start_time_1)
        hp.save_csv("locs.csv", full_d_frame, path_to_data)
    else:  # locations csv exists
        full_d_frame = hp.load_csv("locs.csv", path_to_data)
    print(full_d_frame)
    return

if __name__ == "__main__":
    main()
    #geo_tester()