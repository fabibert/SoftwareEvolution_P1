from quarry import get_modified_files_listed
from quarry import get_modified_files
from quarry import get_change_numbers
from plot import plot


if __name__ == '__main__':

    path = "https://github.com/lutzidan/assignment1-sw-construction"

    get_change_numbers(path)
    get_modified_files(path)
    #get_modified_files_listed(path)
    #plot()

