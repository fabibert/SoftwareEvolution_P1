from quarry import get_modified_files_listed
from quarry import get_modified_files
from plot import plot_from_dictionary
from quarry import get_change_numbers
from plot import plot_csv
from quarry import get_current_sizes
from quarry import filter_commits_by_bugfixes


if __name__ == '__main__':
    path = "https://github.com/mastodon/mastodon.git"

    #get_change_numbers(path)
    #get_modified_files_listed(path)
    #get_modified_files(path)
    #plot_from_dictionary(path)
    #plot_csv()
    #get_current_sizes()
    filter_commits_by_bugfixes(path)


