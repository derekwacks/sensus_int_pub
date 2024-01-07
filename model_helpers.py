import matplotlib.pyplot as plt
import warnings
import matplotlib
warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)

def plotting(dataframe, labels=None):
    if labels is not None and len(labels) == 2:
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])
    x = dataframe.iloc[:, 0]
    y = dataframe.iloc[:, 1]
    plt.plot(x,y, ".")
    plt.show()
    return