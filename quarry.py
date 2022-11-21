from pydriller import Repository
import csv


def get_modified_files_listed(path: str):
    #header = undefined
    data = {}

    i = 0
    for commit in Repository(path).traverse_commits():
        if i >= 1000: break
        for file in commit.modified_files:
            file_path = file.new_path
            if file_path is None: file_path = file.old_path
            if file_path.startswith("app\\services"):
                if data.get(file.filename) is None:
                    data[file.filename] = {}
                data[file.filename][commit.hash] = _count_lines(str(file.content))
        i += 1

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
    header = ['filename', 'total_changes']
    mod_files = []

    i = 0
    for commit in Repository(path).traverse_commits():
        if i >= 1000: break
        for file in commit.modified_files:
            file_path = file.new_path
            if file_path is None: file_path = file.old_path
            if file_path.startswith("app\\services"):
                mod_files.append(file.filename)
        i += 1

    file_set = set(mod_files)
    counts = {}
    counter = 0
    for file in file_set:
        for copy in mod_files:
            if copy == file:
                counter = counter + 1
        counts[file] = counter
        counter = 0

    listed_data = []
    for k, v in counts.items():
        listed_data.append([k, v])

    with open('change_numbers.csv', 'w', encoding='UTF8', newline='') as f:
         writer = csv.writer(f)
         writer.writerow(header)
         writer.writerows(listed_data)


def get_current_sizes():
    header = ['filename', 'current_size']
    data = []

    try:
        with open('change_log.csv', 'r', encoding='UTF8', newline='') as f:
            filereader = csv.reader(f, delimiter=' ', quotechar='|')
            for row in filereader:
                entry = row[0].split(',')
                data.append([entry[0], entry[-1]])

        with open('current_sizes.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)
    except:
        print("change_log.csv not found")

def _count_lines(content: str) -> int:
    lines = content.split('\\n')
    while '' in lines:
        lines.remove('')
    return len(lines)


