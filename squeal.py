from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


def run_query(database, query):
    '''(Database, str) -> Table
    Given a query on the given database, returns a table representing on the
    table after it is operated on.
    REQ: query follows the format exactly:
         select [column_names] from [tables] where [restrictions]

    >>> database = read_database()
    >>> query = "select * from books"
    >>> table1 = run_query(database, query)
    >>> table1.get_dict() ==(
    {'book.year': [' 1979', ' 2014', ' 2015', ' 2014'],
    'book.title': ['Godel Escher Bach', 'What if?', 'Thing Explainer',
    'Alan Turing: The Enigma'],
    'book.author': [' Douglas Hofstadter', ' Randall Munroe',
    ' Randall Munroe', ' Andrew Hodges']})
    True

    >>> query = "select book.year from books"
    >>> table2 = run_query(database, query)
    >>> table2.get_dict() == (
    {'book.year': [' 1979', ' 2014', ' 2015', ' 2014']})
    True

    >>> query = "select * from books,movies where book.year=m.year"
    >>> table3 = run_query(database, query)
    >>> table3.get_dict() == test_table.get_dict() ==({'m.gross': [],
    'book.author':[],
    'm.title': [],
    'book.year':[],
    'm.year': [],
    'book.title': [],
    'm.studio': []})
    True

    >>> query = "select * from books where book.year>2014"
    >>> table4 = run_query(database, query)
    >>> table4.get_dict() == ({'book.year': [' 2015'],
    'book.author': [' Randall Munroe'], 'book.title': ['Thing Explainer']})
    '''
    # obtain the list of tables from the database
    database_tables = database.get_list_tables()

    # split the query at the spaces, since commands are split by spaces
    split_query = query.split()

    # process the from token from the query
    # split the list of tables at commas that separate them
    table_list = split_query[3].split(",")
    # convert the list of table names into tables
    # loop through the list of table names
    for index in range(len(table_list)):
        # add the extension .csv to the table name in the list
        file_name = table_list[index] + ".csv"
        # convert the table_file to a table
        table_list[index] = read_table(file_name)

    base_table = table_list[0]
    # if there is more than 1 table in the list, use cartesian product on the
    # base table and the tables that follow it until 1 resulting table is left
    if(len(table_list) > 1):
        # loop through the list of tables
        for current_table in range(1, len(table_list)):
            base_table = cartesian_product(base_table,
                                           table_list[current_table])

    # process the where restrictions from the query
    # split the list of restrictions from the query
    # if the "where" token is used
    if("where" in split_query):
        restriction_list = split_query[5].split(",")
        # loop through the constraint_list and apply each constraint from the
        # list to the table
        for index in range(len(restriction_list)):
            constraint(base_table, restriction_list[index])

    # process the select from the query
    # if all columns, indicated with "*"
    if (split_query[1] == "*"):
        column_names = []
        # loop through the base table
        for current_col in range(len(base_table.get_column_list())):
            name = base_table.get_column_list()
            # add the column names to the list of column names
            column_names.append(name[current_col])

    # if specific column names are indicated
    else:
        # split the str of column names at the separator ","
        column_names = split_query[1].split(",")

    # use the select function to only keep the columns that are specified
    select(base_table, column_names)

    return base_table


def constraint(table, restriction):
    '''(Table, str) -> NoneType
    Applies the constraint to the table.
    REQ: restriction must have column names on each side of the operator
    REQ: operator must exist, and must also be either '=' or '>'
    >>> test_table = read_table("books.csv")
    >>> constraint(table, "book.year>2014")
    >>> table.get_dict() == {'book.author': [' Randall Munroe'], 'book.title':
    ['Thing Explainer'], 'book.year': [' 2015']}
    True

    >>> table1 = read_table("books.csv")
    >>> table2 = read_table("movies.csv")
    >>> test_table = cartesian_product(table1, table2)
    >>> constraint(test_table, "book.year=m.year")
    >>> test_table.get_dict() == test_table.get_dict() ==(
    {'m.gross': [], 'book.author': [], 'm.title': [], 'book.year':
    [], 'm.year': [], 'book.title': [], 'm.studio': []})
    True
    '''
    # find what the operator is
    operator = restriction[find_operator(restriction)]
    # split the restriction_list at the operator
    restriction_list = restriction.split(operator)

    # split the restriction at the operator
    split_restriction = restriction.split(operator)
    # keep track of the left/right side of operator
    left_side = split_restriction[0]
    right_side = split_restriction[1]

    # try converting the right_side into a float
    try:
        right_side = float(right_side)
    # if ValueError occurs(cannot be converted to float)
    except ValueError:
        right_side = str(right_side)
    try:
        left_side = float(left_side)
    # if ValueError occurs(cannot be converted to float)
    except ValueError:
        left_side = str(left_side)

    # loop through the table to find the columns where the column items
    # in the restriction_list are
    for col in range(len(list(table.get_keys()))):
        column_list = list(table.get_keys())
        # since restriction_list will always only have 2 indices
        # if the left_side is a column name
        if(left_side == column_list[col]):
            # name of column
            column1 = column_list[col]
        # if the right_side is a column name
        if(str(right_side) == column_list[col]):
            # name of column2
            column2 = column_list[col]
        # else if the right side is a float
        elif(type(right_side) == float):
            # since it is not a column name, pass in the float value istead
            value = right_side

    # if the operator is '='
    if(operator == '='):
        # use the equals function to simplify the table
        table = equals(table, column1, column2)
    # if the operator is '>', the right side will always be a float value
    elif(operator == '>'):
        # use the greater function to simplify the table
        table = greater(table, column1, value)


def find_operator(comparison):
    '''(str) -> int
    Finds and returns the index of the operator in the string passed in.
    REQ: comparison must have '=' or '>' in the str
    REQ: vaules must exist on both sides of the operator
    >>> find_operator("10>9")
    2
    >>> find_operator("a.bcd=e.fgh")
    5
    '''
    # if the operator is '='
    if('=' in comparison):
        operator_index = comparison.find('=')
    # if the operator is '>'
    else:
        operator_index = comparison.find('>')

    return operator_index


def equals(table, column1, column2):
    '''(Table, str, str) -> NoneType
    Helper function that removes the items from the the column in the table
    that don't satisfy the operator.
    >>> column1 = m.title
    >>> column2 = o.title
    >>> table1 = read_table("movies.csv")
    >>> table2 = read_table("oscars.csv")
    >>> test_table = cartesian_product(table1, table2)
    >>> equals(test_table, column1, column2)
    >>> test_table.get_dict() == ({'o.title': ['Toy Story 3',
    'The Lord of the Rings: The Return of the King', 'Titanic',
    'Titanic'], 'm.title': ['Titanic', 'Titanic',
    'The Lord of the Rings: The Return of the King', 'Toy Story 3'],
    'o.year': ['2010', '2003', '1997', '1997'],
    'm.year': ['1997', '1997', '2003', '2010'],
    'm.studio': ['Par.', 'Par.', 'NL', 'BV'],
    m.gross': ['2186.8', '2186.8', '1119.9', '1063.2'],
    'o.category': ['Animated Feature Film', 'Directing',
    'Directing', 'Best Picture']})
    True
    '''
    column1_items = table.get_column_values(column1)
    column2_items = table.get_column_values(column2)
    # number of items in both columns are same
    num_rows = table.num_rows()
    # list of items to remove
    column_list = []
    remove_list = []
    # loop through the items in each column
    for item in range(num_rows):
        # if the two items are not equal at that row
        if(column1_items[item] != column2_items[item]):
            # store columns and items to be removed later
            for col in range(len(table.get_column_list())):
                column = table.get_column_list()[col]
                remove = table.get_column_values(column)[item]
                column_list.append(column)
                remove_list.append(remove)

    # remove all the items
    for i in range(len(column_list)):
        table.remove_column_item(column_list[i], remove_list[i])


def greater(table, column1, value):
    '''(Table, str, int) -> NoneType
    Helper function that removes the items from the the column in the table
    that don't satisfy the operator.
    >>> test_table = read_table("books.csv")
    >>> greater(test_table, "book.year", 2014)
    >>> test_table.get_dict() == ({'book.year': [' 2015'],
    'book.author': [' Randall Munroe'], 'book.title': ['Thing Explainer']})
    True
    '''
    column1_items = table.get_column_values(column1)
    # number of items in both columns are same
    num_rows = table.num_rows()
    # list of items to remove
    column_list = []
    remove_list = []
    # loop through the items in each column
    for item in range(num_rows):
        # if the two items are not equal at that row
        if(not(float(column1_items[item]) > value)):
            # store the columns and items to be removed later
            for col in range(len(table.get_column_list())):
                column = table.get_column_list()[col]
                remove = table.get_column_values(column)[item]
                column_list.append(column)
                remove_list.append(remove)

    # remove all the items
    for i in range(len(column_list)):
        table.remove_column_item(column_list[i], remove_list[i])


def select(table, list_columns):
    '''(Table, list of str) -> NoneType
    Given a table and a list of column names, remove the columns that are not
    specified by the query.
    REQ: the values in list_columns must exist in the tables specified
    >>> table1 = read_table("books.csv")
    >>> test_table = select(test_table, ["book.year"])
    >>> test_table.get_dict() == (
    {'book.year': [' 1979', ' 2014', ' 2015', ' 2014']})
    True
    '''
    table_cols = table.get_column_list()
    # loop through the table's columns
    for col in range(len(table_cols)):
        if(not(table_cols[col] in list_columns)):
            table.remove_column(table_cols[col])

    return table


def cartesian_product(table1, table2):
    '''(Table, Table) -> Table
    Returns a table where each row in the first table is paired with every row
    in the second table.
    >>> table1 = read_table("books.csv")
    >>> table2 = read_table("movies.csv")
    >>> test_table = cartesian_product(table1, table2)
    >>> test_table.get_dict() == ({'m.gross': ['2186.8', '1119.9', '1063.2',
    '2186.8', '1119.9', '1063.2', '2186.8', '1119.9', '1063.2', '2186.8',
    '1119.9', '1063.2'], 'm.studio': ['Par.', 'NL', 'BV', 'Par.', 'NL', 'BV',
    'Par.', 'NL', 'BV', 'Par.', 'NL', 'BV'], 'book.author':
    [' Douglas Hofstadter', ' Douglas Hofstadter', ' Douglas Hofstadter',
    ' Randall Munroe', ' Randall Munroe', ' Randall Munroe', ' Randall Munroe',
    ' Randall Munroe', ' Randall Munroe', ' Andrew Hodges', ' Andrew Hodges',
    ' Andrew Hodges'], 'm.title': ['Titanic', 'The Lord of the Rings:
    The Return of the King', 'Toy Story 3', 'Titanic', 'The Lord of the Rings:
    The Return of the King', 'Toy Story 3', 'Titanic', 'The Lord of the Rings:
    The Return of the King', 'Toy Story 3', 'Titanic', 'The Lord of the Rings:
    The Return of the King', 'Toy Story 3'], 'book.year': [' 1979', ' 1979',
    ' 1979', ' 2014', ' 2014', ' 2014', ' 2015', ' 2015', ' 2015', ' 2014',
    ' 2014', ' 2014'], 'book.title': ['Godel Escher Bach', 'Godel Escher Bach',
    'Godel Escher Bach', 'What if?', 'What if?', 'What if?', 'Thing Explainer',
    'Thing Explainer', 'Thing Explainer', 'Alan Turing: The Enigma',
    'Alan Turing: The Enigma', 'Alan Turing: The Enigma'], 'm.year':
    ['1997', '2003', '2010', '1997', '2003', '2010', '1997', '2003', '2010',
    '1997', '2003', '2010']}
    True

    >>> table1 = Table()
    >>> table2 = Table()
    >>> test_table = cartesian_product(table1, table2)
    >>> test_table.get_dict() == {}
    True
    '''
    # make an empty table to store the product in
    product_table = Table()

    # add the two column headers together
    product_headers = table1.get_column_list() + table2.get_column_list()
    product_table.set_column_list(product_headers)
    # convert the set of column names in both tables into a list
    table1_keys = list(table1.get_keys())
    table2_keys = list(table2.get_keys())

    # loop through the first table
    for key in range(len(table1_keys)):
        # create the column name in the product_table
        product_table.add_column_names(table1_keys[key])
        # the resultant table will always have the amount of numrow table1
        # * table2 numrow
        # loop through the rows in the first table
        for row1 in range(table1.num_rows()):
            # loop through the rows in the second table
            for row2 in range(table2.num_rows()):
                current_item = table1.get_column_values(table1_keys[key])[row1]
                product_table.add_column_values(table1_keys[key], current_item)
    for key in range(len(table2_keys)):
        # create the column name in the product_table
        product_table.add_column_names(table2_keys[key])
        # the resultant table will always have the amount of numrow table1
        # * table2 numrow
        # loop through the rows in the first table
        for row1 in range(table1.num_rows()):
            # loop through the rows in the second table
            for row2 in range(table2.num_rows()):
                current_item = table2.get_column_values(table2_keys[key])[row2]
                product_table.add_column_values(table2_keys[key], current_item)

    return product_table


if(__name__ == "__main__"):
    query = input("Enter a SQuEaL query, or a blank line to exit:")
    database = read_database()
    # loop will exit once a blank line is entered.
    while(query != ''):
        result = run_query(database, query)
        print('')
        result.print_csv()
        query = input("\nEnter a SQuEaL query, or a blank line to exit:")
