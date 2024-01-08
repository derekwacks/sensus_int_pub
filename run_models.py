"""
corr_amenity_queues.py
"""
import argparse
import pandas as pd
import numpy as np
import helpers as hp
import data_merger as dm
import models as mdls
import model_helpers as mdlhp


def analyze(f_name, path):
    """
    Initial analysis ...
    :param f_name: name of csv file to load
    :param path: path to csv file
    :return: None
    """
    merged_data = hp.load_data(f_name, path)
    if not merged_data.empty:
        print(merged_data)
        avg = merged_data["NaturalAmenityTier"].mean()
        print("Mean", avg)
        counts = merged_data.NaturalAmenityTier.value_counts()
        print(counts)
    return


def queue_type(choice=3):
    """
    Sets file name and CSV output name based on Choice
    :param choice: int 1,2 or 3 -> withdrawn, in-service, or currently in the queue
    :return: f_name, m_name=file name and CSV output name
    """
    f_name, m_name = "", ""
    if choice == 1:
        f_name = "NYISO_withdrawn.csv"
        m_name = "merged_withdrawn.csv"
    elif choice == 2:
        f_name = "NYISO_inservice.csv"
        m_name = "merged_in_service.csv"
    elif choice == 3:
        f_name = "NYISO_active.csv"
        m_name = "merged_in_queue.csv"
    return f_name, m_name


def equal_withdrawn_and_inservice(df):
    """
    Include equal number of withdrawn and in-service
    :param df: dataframe of withdrawn and in-service projects
    :return: new concatenated dataframe of equal number of withdrawn and in-service projects
    """
    withdrawn_row_count = df.loc[df['indicator']==0].shape[0]
    inservice_row_count = df.loc[df['indicator']==1].shape[0]
    lesser = min(withdrawn_row_count, inservice_row_count)
    withdrawn = df.loc[df['indicator']==0][:lesser].copy()
    service = df.loc[df['indicator']==1][:lesser].copy()
    returning_df = pd.concat([withdrawn, service])
    return returning_df


def format_data_for_exp(f_names, path, cols_to_include):
    """
    :param f_names: names of CSV files to merge with amenity data and create simlified vectors from
    :param path: path to CSV files
    :return: pandas df of merged data frame as matrix with amenity index and indicator
    """
    f_names = dm.add_amenity_data_driver(f_names, path)
    f_names_indic_tuples = dm.add_indicators(f_names)
    merged_data = dm.create_matrix(f_names_indic_tuples, path, cols_to_include)
    equalize = False
    if equalize:
        merged_data = equal_withdrawn_and_inservice(merged_data)
    merged_data = merged_data.sample(frac=1)  # Randomize rows
    return merged_data


def main(model_choice):
    path = "/Users/derekwacks/Documents/Interconnection/code/data/training"
    f_names = ["NYISO_withdrawn.csv", "NYISO_inservice.csv",
               "ISONE_withdrawn.csv", "ISONE_inservice.csv",
               "MISO_withdrawn.csv", "MISO_inservice.csv",
               "PJM_withdrawn.csv", "PJM_inservice.csv",]
    cols_to_include = ['NaturalAmenityTier']#, 'Opposed']
    merged_data = format_data_for_exp(f_names, path, cols_to_include)
    print("merged_data:\n", merged_data)
    print("withdrawn count:", merged_data['indicator'].value_counts()[0])
    print("in service count:", merged_data['indicator'].value_counts()[1])

    #probs = create_probs(merged_data)
    #mdlhp.plotting(probs, labels=["Amenity Index", "Probability of Success"])
    if model_choice == 0:
        mdls.bayes(merged_data)
    elif model_choice == 1:
        mdls.nb_param_selector_and_driver(merged_data)
    elif model_choice == 2:
        mdls.regress_linear(merged_data)
    elif model_choice == 3:
        mdls.regress_statsmodel(merged_data, model_type="probit", plotting_flag=True)
    elif model_choice == 4:
        mdls.regress_statsmodel(merged_data, model_type="logit", plotting_flag=False)
    else:
        raise ValueError('Only select a model choice in [0,4]')
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and test a selected model")
    parser.add_argument("--model", required=True, type=int)
    args = parser.parse_args()
    main(args.model)

