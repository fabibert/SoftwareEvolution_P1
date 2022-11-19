from pydriller import *
from pydriller import Repository
import csv

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
    header = ['commit', 'changed_files']
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
        writer.writerow(header)
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
