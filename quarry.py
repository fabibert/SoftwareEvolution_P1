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
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(header_column)
    i = 0
    #[list.insert(0, header_column[++i]) for list in matrix]
    for list in matrix:
        list.insert(0, header_column[i])
        i = i+1


    #matrix[0].insert(0, header_column)

    print(matrix)

    #matrix_names = [[k for k, v in data.items()],[[y for x, y in v.items()] for k, v in data.items()]]

    #matrix_names2 = [[y for x, y in v.items()] for k, v in data.items()]
    # for i in range(len(matrix_names2)):
    #     for k, v in data.items():
    #         matrix_names2[i].insert(0, k)

    #for k, v in data.items():

    #[{try: list.insert(0, "hallo") except: list+1} for list in matrix_names2]

    #print(matrix_names2)

    matrix_names3 = [[[k , [y for x,y in v.items()]] for k,v in data.items()]]
    #print(matrix_names3)





    # people = {1: {'Name': 'John', 'Age': '27', 'Sex': 'Male'},
    #           2: {'Name': 'Marie', 'Age': '22', 'Sex': 'Female'}}
    #
    # matrix = [][]
    # for p_id, p_info in people.items():
    #     print("\nPerson ID:", p_id)
    #
    #     for key in p_info:
    #         print(key + ':', p_info[key])



    # matrixed_data = []
    # #for entry in list
    # for entry in listed_data():
    #     for k, v in entry.items():
    #         matrixed_data.append([k, v])
    # print(matrixed_data)


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


