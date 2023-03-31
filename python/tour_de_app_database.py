import sqlite3
from typing import Dict, Tuple, List, Any
from Errors import *
from constants import *
from classes import *
from datetime import datetime

def logger(message):
    current_datetime = datetime.now()
    print(current_datetime.strftime('%m/%d/%Y %H:%M:%S'), message)

def connect_to_database():
    mydb = sqlite3.connect('database', check_same_thread=False, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES, timeout=10)
    mycursor = mydb.cursor()
    mycursor.execute("PRAGMA foreign_keys = ON;")
    return mydb, mycursor


def close_database(mydb, mycursor):
    mycursor.close()
    mydb.close()



class TourDeAppDatabase:
    """Class for database operations.
    Contains methods for select, insert, update and delete operations.
    Methods:
        select - execute select command
        insert - execute insert command
        update - execute update command
        delete - execute delete command
        get_last_added_item - get last added item from table
        check_if_table_exists - check if table exists in database
    """
    
    def select(self, sql_command: str, sql_values = ()) -> SelectQueryResponse:
        """Execute select command.
        Gets sql command and values as arguments.
        Returns SelectQueryResponse object."""

        logger(f"Executing SQL: {sql_command} {sql_values}")
        # -------- create connection --------
        database, cursor = connect_to_database()
        
        # -------- execute command --------
        cursor.execute(sql_command, sql_values)
        response = cursor.fetchall()
        
        # -------- close connection --------
        cursor.close()
        database.close()
        return SelectQueryResponse(response)
        
    
    def insert(self, sql_command: str, sql_values: List[Any], commit:bool = True, return_last_added=True) -> SelectQueryResponse:
        """Execute insert command.
        Gets sql command and values as arguments.
        Returns SelectQueryResponse object."""

        logger(f"Executing SQL: {sql_command} {sql_values}")
        # -------- create connection --------
        database, cursor = connect_to_database()

        # -------- execute command --------
        cursor.execute(sql_command, sql_values)
        if commit:
            database.commit()
        else:
            print('Skipping commit.')
        table_name = sql_command.split()[2]
        if return_last_added:
            last_added_item = self.get_last_added_item(table_name, cursor)
        else:
            last_added_item = None
        
        # -------- close connection --------
        cursor.close()
        database.close()
        return SelectQueryResponse(last_added_item)
    
    def update(self, sql_command: str, sql_values: List[Any], commit:bool = True) -> DatabaseOperationResult:
        """Execute update command.
        Gets sql command and values as arguments.
        Returns DatabaseOperationResult object."""

        logger(f"Executing SQL: {sql_command} {sql_values}")
        # -------- create connection --------
        database, cursor = connect_to_database()

        # -------- execute command --------
        cursor.execute(sql_command, sql_values)
        if commit:
            database.commit()
        else:
            print('Skipping commit.')
        
        # -------- close connection --------
        cursor.close()
        database.close()
        return DatabaseOperationResult('Item updated')
    
    def delete(self, sql_command: str, sql_values: List[Any], commit:bool = True) -> DatabaseOperationResult:
        """Execute delete command.
        Gets sql command and values as arguments.
        Returns DatabaseOperationResult object."""

        logger(f"Executing SQL: {sql_command} {sql_values}")
        # -------- create connection --------
        database, cursor = connect_to_database()

        # -------- execute command --------
        cursor.execute(sql_command, sql_values)
        if commit:
            database.commit()
        else:
            print('Skipping commit.')
        
        # -------- close connection --------
        cursor.close()
        database.close()
        return DatabaseOperationResult('Item deleted')

    def get_last_added_item(self, table_name: str, cursor):
        """Get item last added to database."""
        item_id = str(cursor.lastrowid)
        query = f'SELECT * FROM {table_name} WHERE id=?'
        cursor.execute(query, [item_id])
        response = cursor.fetchall()
        return response
    
    def check_if_id_exist(self, table_name: str, id: int):
        """Check if id exist in table. If not, raise NonExistingKey error. If yes, return True."""
        # -------- create connection --------
        database, cursor = connect_to_database()
        # -------- get all ids from table --------
        sql_command = f'SELECT {ID} FROM {table_name};'
        cursor.execute(sql_command)
        response = cursor.fetchall()
        # -------- check if value exist --------
        for item in response:
            if id == item[0]:
                close_database(database, cursor)
                return True
        raise NonExistingKey(f'{table_name} - id', id)



