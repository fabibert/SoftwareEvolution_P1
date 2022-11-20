from pydriller import Repository
import csv


def get_modified_files_listed(path: str):
    #header = undefined
    data = {}

    for commit in Repository(path).traverse_commits():
        for file in commit.modified_files:
            if data.get(file.filename) is None:
                data[file.filename] = {}
            data[file.filename][commit.hash] = _count_lines(str(file.content))

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


def get_modified_files(path: str):
    #header = ['filename', 'size history']
    data = {}

    for commit in Repository(path).traverse_commits():
        for file in commit.modified_files:
            if data.get(file.filename) is None:
                data[file.filename] = {}
            data[file.filename][commit.hash] = _count_lines(str(file.content))

    listed_data = []
    for k, v in data.items():
        listed_data.append([k, v])

    with open('change_log.csv', 'w', encoding='UTF8', newline='') as f:
         writer = csv.writer(f)
         #writer.writerow(header)
         writer.writerows(listed_data)


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


