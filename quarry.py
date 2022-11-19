from pydriller import *
from pydriller import Repository
import csv
import pandas
import matplotlib as plt

###deprecated
def old_get_modified_files(path: str):
    header = ['commit', 'changed_files']
    data = []

    for commit in Repository(path).traverse_commits():
        entry = [commit.hash]

        changed_files = {}
        for file in commit.modified_files:
            changed_files[file.filename] = _count_lines(str(file.content))

        entry.append(changed_files)
        data.append(entry)

    with open('change_log.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def get_modified_files(path: str):
    #header = ['commit', 'changed_files']
    #header = ['filename']
    data = {}

    for commit in Repository(path).traverse_commits():
        for file in commit.modified_files:
            if data.get(file.filename) is None:
                data[file.filename] = {}
            data[file.filename][commit.hash] = _count_lines(str(file.source_code)) #nested dictionary

    # matrixed_data = []
    # index_counter=0
    # for k, v in data.items():
    #     matrixed_data.append(k)
    #     matrixed_data.append([])
    #     for x,y in v.items():
    #         matrixed_data[index_counter].append(y)
    #     index_counter += 1
    # print(matrixed_data)



    matrix = [[y for x, y in v.items()] for k, v in data.items()]
    header_column = []
    for k, v in data.items():
        header_column.append(k)

    i = 0
    for list in matrix:
        list.insert(0, header_column[i])
        i = i+1

    print(matrix)

    with open('change_log.csv', 'w', encoding='UTF8', newline='') as f:
         writer = csv.writer(f)
         #writer.writerow(header)
         writer.writerows(matrix)

def create_plot():
    df = pandas.read_csv("change_log.csv", header=1)
    #csv file to panda
    plt.figure(figsize=(10, 10))
    plt.ylabel('Absolute Power (log)', fontsize=12)
    plt.xlabel('Frequencies', fontsize=12)
    plt.plot(df.columns, df.mean())
    #ignore key values
    #just get loc and plot



def get_change_numbers(path: str):
    mod_files = []
    for commit in Repository(path).traverse_commits():
        for file in commit.modified_files:
            mod_files.append(file.filename)
    file_set = set(mod_files)
    counts = {}
    counter = 0
    for file in file_set:
        for copy in mod_files:
            if copy == file:
                counter = counter + 1
        counts[file] = counter
        counter = 0

    print(counts)

def _count_lines(content: str) -> int:
    lines = content.split('\\n')
    while '' in lines:
        lines.remove('')
    return len(lines)


