import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB, CategoricalNB
import matplotlib.pyplot as plt
import warnings
import matplotlib
warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)
import statsmodels.api as sm
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import LinearRegression, LogisticRegression


def create_probs(merged_data):
    """
    :param merged_data: n x 2 matrix where 1st column is amenity value [1,5], and second is indicator value [0,1]
    :return:
    """
    # Collecting data
    amenity_counts = merged_data.NaturalAmenityTier.value_counts()  # counts of amenity indicies across all data
    amenity_counts = pd.DataFrame(amenity_counts)
    num_points = amenity_counts.sum()  # count of all points
    in_service_data = merged_data.loc[merged_data["indicator"] == 1]  # all data, filtered for successful projects
    success_counts = in_service_data.NaturalAmenityTier.value_counts()  # counts of amenity indicies across successful projects
    success_counts = pd.DataFrame(success_counts)
    num_success = success_counts.sum()  # count of successful projects
    # Assembling bayes rule
    pr_a_given_s = success_counts / num_success  # probability of each amenity value given the amenity value is from a successful proj.
    p_s = num_success / num_points  # probability of a successful project
    p_a = amenity_counts / num_points  # probability of getting each amenity value
    freqs = pr_a_given_s * p_s / p_a  # bayes rule
    freqs = freqs.reset_index()  # include amenity values as a column
    print(freqs)
    print(amenity_counts)
    return freqs


def rebuild_into_vec(amenity):
    """
    Function to apply to pandas data frame cell, turns amenity index into indicator vector
    3 -> 0,0,1,0,0,0,0
    :param amenity: int amenity value
    :return: vector with 1 at amenity index (indexed from 1)
    """
    val = int(amenity)
    vec = [0]*7
    vec[val-1] = 1
    vec = np.array(vec)
    return vec


def naive_bayes(merged_data, params):
    data_version = params["data_version"]
    printing = params["printing"]
    model_type = params["model_type"]
    if data_version == "vectorized":  # Create each x feature as an indicator vector
        merged_data["vec"] = merged_data["NaturalAmenityTier"].apply(rebuild_into_vec)
        x_orig = merged_data["vec"]
        x = np.stack(x_orig, axis=0)
    elif data_version == "numerical":  # Create each x feature as a float value amenity tier
        x_orig = merged_data.iloc[:, 0]
        x = np.array(x_orig).reshape((-1, 1))
    y_orig = merged_data.iloc[:, 1]
    y = np.array(y_orig)
    # Create train and test sets
    test_split = int(len(x) / 5 * 4)  # 80/20 split
    x_test = x[test_split:]
    y_test = y[test_split:]
    x = x[:test_split]
    y = y[:test_split]
    # Create and fit model
    if model_type == "multi":
        model = MultinomialNB().fit(x, y)
    elif model_type == "categ":
        model = CategoricalNB().fit(x, y)
    # Make predictions on test set
    yhat_prob = model.predict_proba(x_test)  # make a probabilistic prediction
    yhat_class = model.predict(x_test)  # make a classification prediction
    if printing:
        print("Sample", x_test, y_test)
        print("Predicted Probabilities: ", yhat_prob)
        print("Predicted Class: ", yhat_class)
        print("True Class: ", y_test)
        print("PARAMS", model.get_params(), "\n")
    return


def nb_param_selector_and_driver(merged_data, choice=1):
    """
    :param merged_data:
    :param choice: parameter set indicator variable (1 == default)
    :return: None
    Naive bayes driver function
    # # # # # # # # # # # # # # #
    data_version = "vectorized" to use be able to use multinomial, or "numerical" to use categorical
    printing = True, False
    model_type = "categ", "multi"
    # # # # # # # # # # # # # # #
    """
    params = {
        "data_version": "numerical",
        "printing": False,
        "model_type": "categ"
    }
    if choice == 2:
        params["data_version"] = "vectorized"
        params["printing"] = True
        params["model_type"] = "categ"
    elif choice == 3:
        params["data_version"] = "vectorized"
        params["printing"] = True
        params["model_type"] = "multi"
    elif choice == 4:
        params["data_version"] = "vectorized"
        params["printing"] = True
        params["model_type"] = "categ"
    elif choice == 5:
        params["data_version"] = "numerical"
        params["printing"] = True
        params["model_type"] = "categ"
    elif choice == 6:
        params["data_version"] = "vectorized"
        params["printing"] = True
        params["model_type"] = "multi"
    naive_bayes(merged_data, params)
    return


def regress_linear(dataframe, model_type="linear", plotting_flag=False):
    x_orig = dataframe.iloc[:, 0]  # Natural Amenity Index
    y_orig = dataframe.iloc[:, 1]  # Withdrawn indicator
    x = np.array(x_orig).reshape((-1, 1))
    y = np.array(y_orig)
    test_split = int(len(x) / 5 * 4)
    x_test = x[test_split:]
    y_test = y[test_split:]
    x = x[:test_split]
    y = y[:test_split]
    if model_type == "linear":
        model = LinearRegression().fit(x, y)
    else:
        model = LogisticRegression().fit(x,y)

    print("\nTesting")
    r_sq = model.score(x_test, y_test)
    print(f"coefficient of determination: {r_sq}")
    print(f"slope: {model.coef_}")
    print(f"intercept: {model.intercept_}")

    # Make predictions of y using the fitted linear model
    pred = model.predict(x_test)
    # Calculate the residuals: difference between the predictions and the real outcome y
    residuals = y_test - pred

    if plotting_flag:
        # scatter plot of the independent variable x and the residuals
        plt.scatter(y=residuals, x=x_test)
        plt.ylabel('Residuals')
        plt.xlabel('Independent variable x')
        plt.show()
        # evaluate the distribution of the residuals
        #sns.distplot(residuals, bins=30)
        plt.xlabel('Residuals')
    return


def svm_model(dataframe, path):
    x_orig = dataframe.iloc[:, 0]
    y_orig = dataframe.iloc[:, 1]
    x = np.array(x_orig).reshape((-1, 1))
    y = np.array(y_orig)

    """
    frac_test_split = 0.33
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=frac_test_split)#, random_state=blobs_random_seed)
    d_name = path+'svm_data.npy'
    print(X_train, X_test, y_train, y_test, "\n\n")
    #np.save(d_name, (X_train, X_test, y_train, y_test))
    #X_train, X_test, y_train, y_test = np.load(d_name, allow_pickle=True)
    plt.scatter(X_train[:, 0], X_train[:, 1])
    """

    plt.plot(x_orig, y_orig, ".")
    plt.xlabel('Amenity Tier')
    plt.ylabel('Success Indicator')
    plt.show()


def regress_statsmodel(dataframe, model_type="logit", plotting_flag=False):
    x_orig = dataframe.iloc[:, 0]  # Natural Amenity Index
    y_orig = dataframe.iloc[:, 1]  # Withdrawn indicator
    x = np.array(x_orig).reshape((-1, 1))
    y = np.array(y_orig)
    test_split = int(len(x) / 5 * 4)  # 80/20 split
    x_test = x[test_split:]
    y_test = y[test_split:]
    x = x[:test_split]
    y = y[:test_split]

    # Train
    if model_type == "probit":
        model = sm.Probit(y, x)
    elif model_type == "logit":
        model = sm.Logit(y, x)

    logistic_reg = model.fit()
    print(logistic_reg.summary())

    # Test
    y_hat = logistic_reg.predict(x_test)
    predictions = list(map(round, y_hat))
    print("Test accuracy=", accuracy_score(y_test, predictions))
    x_test = x_test.flatten()
    cm = pd.crosstab(y_test, predictions)
    print("Confusion Matrix\n", cm)
    if plotting_flag:
        # scatter plot of the independent variable x and the residuals
        residuals = y_test - predictions
        plt.scatter(y=residuals, x=x_test)
        plt.ylabel('Residuals')
        plt.xlabel('Independent variable x')
        plt.show()
        plt.xlabel('Residuals')
    return
