from record import Record
from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable
from tour_de_app_database import TourDeAppDatabase
from programmer import Programmer

# ========================== TESTING ==========================
import mysql.connector
from login import *


mydb = mysql.connector.connect(
    host=HOST,
    user=DATABASE_USER,
    password=PASSWORD,
    database = DATABASE
)

mycursor = mydb.cursor()



instance1 = Programmer(id=5, name='Lubomír', surname='Janda')
instance2 = Programmer(id=5, surname='Janda')
instance3 = Programmer(id=5, name='Lubomír')



# -------- testing get --------

get_query = Record.generate_select_query()
assert get_query == 'SELECT * FROM records;', 'Get querry is wrong'


# -------- testing post --------

assert instance1.generate_insert_query()==('INSERT INTO programmers (name, surname) VALUES (%s, %s)', ['Lubomír', 'Janda']), 'post querry is wrong'
assert instance2.generate_insert_query().value_name == 'name', 'name query is wrong'
assert instance3.generate_insert_query().value_name == 'surname', 'surname query is wrong'


# -------- testing put --------
try:
    instance1.generate_update_query()
except EmptyRequest:
    pass
else:
    print('Empty exception failed.')
instance1.update_value(NAME, 'Pavel')
assert instance1.generate_update_query() == ('UPDATE programmers SET name = %s WHERE id = %s', ['Pavel', 5]), 'update querry'

instance1.update_value(SURNAME, 'Šťastný')
assert instance1.generate_update_query() == ('UPDATE programmers SET name = %s,  surname = %s WHERE id = %s', ['Pavel', 'Šťastný', 5]), 'update querry'


# query, values = instance1.generate_put_query()
# print(query)
# mycursor.execute(query, values)
# mycursor.execute(get_query)
# print(mycursor.fetchall())


# -------- testing delete --------
assert instance1.generate_delete_query() == ('DELETE FROM programmers WHERE id = %s;', [5]), instance1.generate_delete_query()


# -------- test record to str --------

assert str(instance1) == '{"id": 5, "name": "Pavel", "surname": "Šťastný"}', 'Error in converting record to string.'
assert str(instance2) == '{"id": 5, "name": null, "surname": "Janda"}', 'Error in converting record to string.'
assert str(instance3) == '{"id": 5, "name": "Lubomír", "surname": null}', 'Error in converting record to string.'

# -------- test if all obligatory arguments passed --------
assert instance1.check_if_all_obligatory_values_provided() == True, 'Error in obligatory values check.'
assert instance2.check_if_all_obligatory_values_provided() == False, 'Error in obligatory values check.'
assert instance3.check_if_all_obligatory_values_provided() == False, 'Error in obligatory values check.'
