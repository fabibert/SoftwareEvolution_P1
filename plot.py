from pydriller import Repository
import pandas as pd
import matplotlib.pyplot as plt
from quarry import _count_lines
from os import listdir
from os.path import isfile, join


def plot_from_dictionary(path):
    data = {}

    #reusing antons commit to dictionary code
    counter = 0
    for commit in Repository(path).traverse_commits():
        counter = counter + 1
        if(counter%100 == 0):
            print(counter, "/", "12366") #display progress
        for file in commit.modified_files:
            file_path = file.new_path
            if file_path is None: file_path = file.old_path
            if file_path.startswith("app\\services"):
                if data.get(file.filename) is None:
                    data[file.filename] = {}
                data[file.filename][commit.hash] = _count_lines(str(file.content))  # nested dictionary

    #preparing dataframe from dictionary
    df_dict = pd.DataFrame.from_dict(data).T
    df_dict = df_dict.T.fillna(method='ffill').T
    df_dict = pd.DataFrame.from_dict(data).T
    df_dict = df_dict.fillna(value=0)
    print("saving dictionary")
    df_dict.to_csv("dict_frame_filtered.csv")

    #create plot from dataframe
    plt.figure(figsize=(20, 12), dpi=80)
    for index, column in df_dict.iterrows():
        plt.plot(column, label=index)

    plt.legend()
    plt.savefig("graph_dict.pdf")
    plt.show()


def plot_csv():
    df_dict = pd.read_csv("dict_frame_filtered.csv", index_col=0)
    df_dict = df_dict.head(10)
    df_dict = df_dict.loc[:, (df_dict != 0).any(axis=0)] #drop commits where loc is all zero

    # create plot from dataframe
    plt.figure(figsize=(20, 12), dpi=80)
    for index, column in df_dict.iterrows():
        plt.plot(column, label=index)

    plt.legend()
    plt.savefig("graph_dict.pdf")
    plt.show()
