from quarry import get_modified_files
from quarry import get_change_numbers



if __name__ == '__main__':

    path = "https://github.com/lutzidan/assignment1-sw-construction.git"

    get_change_numbers(path)
    get_modified_files(path)


