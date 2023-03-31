from constants import *
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
import json
import copy


class DatabaseTable():
    """Abstract class for database tables.
    Contains methods for generating queries
    Stores values of certain record from database.
    Methods:
        init_from_tuple - initializes values from tuple
        init_from_request - initializes values from request
        get_values_by_name - returns value by name of the value
        generate_select_query - generates query for selecting all records from table
        generate_insert_query - generates query for inserting record into table
        generate_update_query - generates query for updating record in table
        generate_delete_query - generates query for deleting record from table
        filter_by_column_value - generates query to filter by column value.
        check_if_all_obligatory_values_provided - checks if all obligatory values are provided.
        update_value - Updates value of the object and sets it as updated.
        set_all_values_updated - sets all values updated flag to True.
        __str__ - returns string representation of object in json format.
        __dict__ - returns dictionary representation of object.
        """
    RATING_MINIMAL_VALUE: int
    RAGING_MAXIMAL_VALUE: int
    TABLE_NAME: str
    VALUE_INFO: Dict[str, Value]
    FOREIGN_KEYS: List[Tuple[str, str]]

    def __init__(self) -> None:
        self.values: Dict[str, Value]


    def init_from_tuple(self, tuple: Tuple[Any], ignore_values_with_not_store_flag: bool = False):
        """Initializes object values from tuple.
        If ignore_values_with_not_store_flag is True, then values with do_store flag set to False will be ignored.
        ignore_values_with_not_store_flag is set to True when initializing from parameters.
        
        Args:
            tuple (Tuple[Any]): Tuple with values.
            ignore_values_with_not_store_flag (bool, optional): If True, values with do_store flag set to False will be ignored. Defaults to False.
            
        """
        value_keys = list(self.VALUE_INFO.keys())
        i = 0
        self.values = {}
        skipped_values = 0
        while i < len(value_keys):
            value_name = value_keys[i]
            value_value = tuple[i-skipped_values]
            value_instance = copy.copy(self.VALUE_INFO[value_name])
            if self.VALUE_INFO[value_name].do_store or ignore_values_with_not_store_flag:
                value_instance.force_update(tuple[i-skipped_values])
            else:
                skipped_values += 1
            self.values[value_name] = value_instance
            i += 1
    
    def init_from_request(self, data: Dict[str, Any], id: int = None):
        """Initializes object values from request.
        Args:
            data (Dict[str, Any]): Request data.
            id (int, optional): ID of the object. Defaults to None.
        """
        data[ID] = id
        value_keys = list(self.VALUE_INFO.keys())
        provided_data_keys = list(data.keys())
        self.values = {}
        for key in value_keys:
            value_instance = copy.copy(self.VALUE_INFO[key])
            if key in provided_data_keys:
                value_instance.force_update(data[key], set_updated=True)
            else:
                value_instance.force_update(None)
            self.values[key] = value_instance

        
    def get_value_by_name(self, name: str) -> Value:
        """Returns value by name of the value.
        Args:
            name (str): Name of the value."""
        for value in self.values:
            if value.name == name:
                return value

    def generate_insert_query(self, ignore_primary_key=True) -> Tuple[str, List[Any]]:
        """Generates insert query.
        Args:
            ignore_primary_key (bool, optional): If True, primary key will be ignored. Defaults to True.
        Returns:
            Tuple[str, List[Any]]: Tuple with query and values to be inserted into query string.
        Raises:
            MissingOblitagoryValue: If obligatory value is missing.
        """
        sql_header = f'INSERT INTO {self.TABLE_NAME} '
        sql_values = []
        columns = '('
        values_template = '('


        for value_name in self.values.keys():
            value = self.values[value_name]
            if ignore_primary_key:
                if value.primary_key or not value.do_store:
                    continue

            if not value.value == None:
                columns += value_name + ', '
                values_template += '?, '
                if type(value.value) == list:
                    sql_values.append(json.dumps(value.value))
                else:
                    sql_values.append(value.value)
            elif value.is_obligatory:
                raise MissingOblitagoryValue(value_name)
        
        columns = columns[:-2] + ')'
        values_template = values_template[:-2] + ')'
        
        sql = sql_header + columns + ' VALUES ' + values_template
        return sql, sql_values

    def generate_update_query(self):
        """Generates update query.
        Returns:
            Tuple[str, List[Any]]: Tuple with query and values to be inserted into query string.
        Raises:
            EmptyRequest: If there are no values to update.
        """
        sql_header = f'UPDATE {self.TABLE_NAME} SET'
        sql_values = []


        for value_name in self.values.keys():
            value = self.values[value_name]
            if value.primary_key or not value.do_store:
                continue

            if value.updated:
                value.updated=False
                sql_header += ' ' + value_name + ' = ?, '
                if type(value.value) == list:
                    sql_values.append(json.dumps(value.value))
                else:
                    sql_values.append(value.value)
        
        if len(sql_values) == 0:
            raise EmptyRequest
        sql_values.append(self.values[ID].value)
        sql = sql_header[:-2] + f' WHERE id = ?'

        
        
        return sql, sql_values
    

    def filter_by_column_value(self, column_name: str, value: Any):
        """Generates query to filter by column value.
        Args:
            column_name (str): Name of the column.
            value (Any): Value of the column.
            Returns:
            Tuple[str, List[Any]]: Tuple with query and values to be inserted into query string.
        """
        return f'SELECT * FROM {self.TABLE_NAME} WHERE {column_name} = ?;', [value]



    def generate_delete_query(self):
        """Generates delete query.
        Returns:
            Tuple[str, List[Any]]: Tuple with query and values to be inserted into query string.
        """
        return f'DELETE FROM {self.TABLE_NAME} WHERE id = ?;', [self.values[ID].value]

    def __str__(self) -> str:
        """Returns string representation of the object in json format.
        Returns:
            str: String representation of the object in json format.
        """
        output_dict = {}
        for value_name in self.values.keys():
            value = self.values[value_name]
            if not value.is_metadata and not value.private:
                output_dict[value_name] = value.value
        
        return json.dumps(output_dict, ensure_ascii=False)
    
    def update_value(self, property_name: str, updated_value_value):
        """Updates value of the object. and sets it as updated."""
        self.values[property_name].value = updated_value_value
        self.values[property_name].updated = True
    
    def check_if_all_obligatory_values_provided(self):
        """Checks if all obligatory values are provided.
        Returns:
            bool: True if all obligatory values are provided.
        Raises:
            MissingOblitagoryValue: If obligatory value is missing.
        """
        for value_name in self.values.keys():
            value = self.values[value_name]
            if value.is_obligatory and value.value == None:
                raise MissingOblitagoryValue(value_name)
        return True
    
    def __dict__(self):
        """Returns dictionary representation of the object.
        Returns:
            Dict[str, Any]: Dictionary representation of the object.
        """
        output_dict = {}
        for value_name in self.values.keys():
            value = self.values[value_name]
            if not value.is_metadata and not value.private:
                output_dict[value_name] = value.value
        
        return output_dict
    
    
    def set_all_values_updated(self):
        """Sets all values as updated."""
        for key in self.values:
            if not self.values[key].value == None:
                self.values[key].touch()
