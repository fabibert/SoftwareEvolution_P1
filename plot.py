from pydriller import Repository
import pandas as pd
import matplotlib.pyplot as plt
from quarry import _count_lines
from os import listdir
from os.path import isfile, join


def plot():
    # Input
    data_file = 'change_log.csv'
    # Delimiter
    data_file_delimiter = ','
    # The max column count a line in the file could have
    largest_column_count = 0

    #counting the longest row in the csv to initialize dataframe
    with open(data_file, 'r') as temp_f: # Loop the data lines
        # Read the lines
        lines = temp_f.readlines()

        for l in lines:
            # Count the column count for the current line
            column_count = len(l.split(data_file_delimiter)) + 1

            # Set the new most column count
            largest_column_count = column_count if largest_column_count < column_count else largest_column_count

    # Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
    column_names = [i for i in range(0, largest_column_count)]
    column_names[0] = "filenames"

    #create dataframe from csv
    df = pd.read_csv(data_file, header=None, delimiter=data_file_delimiter, names=column_names, index_col=0)

    #create plot
    plt.figure(figsize=(20, 12), dpi=80)
    for index, column in df.iterrows():
        plt.plot(column, label=index)

    plt.legend()
    plt.savefig("graph.pdf")
    plt.show()


def plot_from_dictionary():
    path = "https://github.com/mastodon/mastodon.git"
    # header = ['commit', 'changed_files']
    # header = ['filename']
    data = {}

    #reusing antons commit to dictionary code
    commits = Repository(path).traverse_commits()
    number_commits = sum(1 for _ in commits)
    counter = 0
    for commit in Repository(path).traverse_commits():
        counter = counter + 1
        if(counter%100 == 0):
            print(counter, "/", number_commits) #display progress
        for file in commit.modified_files:
            if data.get(file.filename) is None:
                data[file.filename] = {}
            data[file.filename][commit.hash] = _count_lines(str(file.source_code))  # nested dictionary

    #preparing dataframe from dictionary
    df_dict = pd.DataFrame.from_dict(data).T
    df_dict = df_dict.T.fillna(method='ffill').T
    df_dict = pd.DataFrame.from_dict(data).T
    df_dict = df_dict.fillna(value=0)
    print("saving dictionary")
    df_dict.to_csv("dict_frame.csv")

    #change the dictionary to only keep rows of files which are ins services
    mypath = "../mastodon/app/services" #download the repo to a folder next to this one to access list of files in subfolder
    serviceFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(serviceFiles)

    df_dict = df_dict.loc[serviceFiles]
    print("saving filtered")
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
