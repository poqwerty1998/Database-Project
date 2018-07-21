class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self):
        '''(Table, list of str, list of str) -> NoneType
        Creates a table. Values inside every table is stored in a dictionary,
        which has the column as keys mapped to the values that are under that
        column.
        '''
        self._column_list = []
        self._dict_of_columns = {}

    def add_column_names(self, name):
        '''(Table, str) -> NoneType
        Creates a key that maps to an empty list, which stores the values in
        the columns. Name is the column name and also the key.
        '''
        self._dict_of_columns[name] = []

    def add_column_values(self, column, value):
        '''(Table, str, str) -> NoneType
        Adds values to the key inside the table dictionary.
        '''
        # since the column key already maps to a list, append the value
        # to that list
        self._dict_of_columns[column].append(value)

    def get_keys(self):
        '''(Table) -> set
        Returns the keys of the dictionaries, which is also the names of the
        columns.
        '''
        key_set = self._dict_of_columns.keys()
        return key_set

    def get_column_values(self, column):
        '''(Table, str) -> list
        Returns a list that corresponds to the column key from the table.
        '''
        return self._dict_of_columns[column]

    def set_column_list(self, column_list):
        '''(Table, list of str) -> NoneType
        Setter for the column_list values inside a Table.
        '''
        self._column_list = column_list

    def get_column_list(self):
        '''(Table) -> list
        Returns the list of columns for Table.
        '''
        return self._column_list

    def remove_column(self, column):
        '''(Table, str) -> NoneType
        Removes the column in the table.
        '''
        # use the pop method to remove the key
        self._dict_of_columns.pop(column)

    def remove_column_item(self, column, item):
        '''(Table, str, str) -> NoneType
        Removes the item in the column of Table
        '''
        # find the index of the item
        for index in range(len(self._dict_of_columns[column])):
            # if the item is equal to the item at the index in the column
            if(self._dict_of_columns[column][index] == item):
                # remove the item with the pop method
                item_index = index
        self._dict_of_columns[column].pop(item_index)

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        # loop through keys in new_dict
        for key in new_dict:
            value = new_dict[key]
            self._dict_of_columns[key] = value

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self._dict_of_columns

    def print_csv(self):
        '''(Table) -> NoneType
        Print a representation of table in csv format.
        '''
        # no need to edit this one, but you may find it useful (you're welcome)
        dict_rep = self.get_dict()
        columns = list(dict_rep.keys())
        print(','.join(columns))
        rows = self.num_rows()
        for i in range(rows):
            cur_column = []
            for column in columns:
                cur_column.append(dict_rep[column][i])
            print(','.join(cur_column))

    def num_rows(self):
        '''(Table) -> int
        Returns the number of rows in the table.
        '''
        # since all columns have same number of items, using the list from any
        # column will give number of rows.
        for i in self._dict_of_columns:
            num_rows = len(self._dict_of_columns[i])

        return num_rows


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self):
        '''(Database, list of Table) -> NoneType
        Creates a Database with a list of tables in the database. List of
        Table is empty when created.
        '''
        self._list_tables = []
        self._dict_of_tables = {}

    # accessors and mutators for Database class
    def get_list_tables(self):
        '''(Database) -> list of Table
        Returns the list of tables that are contained in the Database.
        '''
        return self._list_tables

    def set_list_tables(self, list_tables):
        '''(Database, list of Table) -> NoneType
        Changes the list_tables value in Database
        '''
        self._list_tables = list_tables

    # Database class methods
    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        # set the keys of new_dict into a list
        list_keys = list(new_dict.keys())
        # loop through keys in new_dict
        for key in range(len(list_keys)):
            self._dict_of_tables[key] = new_dict[key]

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._dict_of_tables
