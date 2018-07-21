# Functions for reading tables and databases

import glob
from database import *
file_list = glob.glob('*.csv')
list_tables = []

# Write the read_table and read_database functions below


def read_table(table_file):
    '''(str) -> Table
    Returns a Table depending on the contents in table_file.

    REQ: table_file is a file name.
    >>> table = read_table("books.csv")
    >>> table.get_dict() == (
    {'book.title': ['Godel Escher Bach', 'What if?',
    'Thing Explainer', 'Alan Turing: The Enigma'],
    'book.year': [' 1979', ' 2014', ' 2015', ' 2014'],
    'book.author': [' Douglas Hofstadter', ' Randall Munroe',
    ' Randall Munroe', ' Andrew Hodges']})
    True
    '''
    # empty list for the information
    table_list = []
    # open the file
    table_file_handle = open(table_file, "r")
    # store the contents of the file in a variable so we can use it
    file_contents = table_file_handle.readlines()

    # loop through the file to separate the columns
    for lines in range(len(file_contents)):
        current_line = file_contents[lines]
        # since each item in the file is separated by a comma (,), split every
        # item at that character value
        split_line = current_line.split(",")
        # add the split line to the empty list
        table_list.append(split_line)

    # close the file after it's used
    table_file_handle.close()
    # create an empty table
    table = Table()

    # since the beginning of each file's contents are the names of the columns,
    # the first element in table_list is what we're looking for.
    column_names = table_list[0]
    rows = table_list[1:]

    # remove the \n next lines in the lists
    # loop through the list of rows/columns
    for col in range(len(column_names)):
        # if \n is in the current column name
        if("\n" in column_names[col]):
            next_line = column_names[col].find("\n")
            column_names[col] = column_names[col][:next_line]
    for row in range(len(rows)):
        # loop through the items in each row
        for item in range(len(rows[row])):
            # if \n is in the current item
            if("\n" in rows[row][item]):
                next_line = rows[row][item].find("\n")
                rows[row][item] = rows[row][item][:next_line]

    table.set_column_list(column_names)

    # add the column names to the table as keys
    for col in range(len(column_names)):
        table.add_column_names(column_names[col])

    # loop through the rest of table_list for the values inside the columns
    for row in range(len(rows)):
        # loop through the items in the row
        for item in range(len(rows[row])):
            # add the item to the key that maps to a list corresponding with
            # the column name
            table.add_column_values(column_names[item], rows[row][item])

    return table


def read_database():
    '''() -> Database
    Returns a database, which contains all the tables in the directory.

    >>> database = read_database()
    >>> database.get_dict() == {}
    True
    '''
    # loop through the file list and run the function read_table on each file
    # in that list to create tables
    for current_file in range(len(file_list)):
        # add the current file in table form to the list of tables
        list_tables.append(read_table(file_list[current_file]))

    # create the database object
    database = Database()
    # set the list of tables in the database
    database.set_list_tables(list_tables)

    return database
