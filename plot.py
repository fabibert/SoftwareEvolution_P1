def plot():
    import pandas
    import matplotlib.pyplot as plt
    # Input
    data_file = 'change_log.csv'

    # Delimiter
    data_file_delimiter = ','

    # The max column count a line in the file could have
    largest_column_count = 0

    # Loop the data lines
    with open(data_file, 'r') as temp_f:
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

    # Read csv
    df = pandas.read_csv(data_file, header=None, delimiter=data_file_delimiter, names=column_names, index_col=0)

    plt.figure(figsize=(20, 12), dpi=80)
    for index, column in df.iterrows():
        plt.plot(column, label=index)
    plt.legend()

    plt.savefig("graph.pdf")
    plt.show()