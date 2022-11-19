from quarry import get_modified_files
from quarry import get_change_numbers


if __name__ == '__main__':

    path = "https://github.com/Xyarlo/SoPra-Server.git"

    get_change_numbers(path)
    get_modified_files(path)
