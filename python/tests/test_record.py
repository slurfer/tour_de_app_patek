from record import Record
from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable
from tour_de_app_database import TourDeAppDatabase

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




instance1 = Record(id=96, datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, rating=3, programmer_id=2, description='Ahoj')
instance2 = Record(datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, rating=3, programmer_id=2, description='Ahoj')
instance3 = Record(id=0, programming_language='python', minutes_spent=20, rating=3, programmer_id=2, description='Ahoj')
instance4 = Record(id=0, datetime="2022-12-28 17:05:11", minutes_spent=20, rating=3, programmer_id=2, description='Ahoj')
instance5 = Record(id=0, datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, programmer_id=2, description='Ahoj')
instance6 = Record(id=0, datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, rating=3, description='Ahoj')
instance7 = Record(id=0, datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, rating=3, programmer_id=2)



# -------- testing get --------

get_query = Record.generate_select_query()
assert get_query == 'SELECT * FROM records;', 'Get querry is wrong'


# -------- testing post --------

assert instance1.generate_insert_query()==('INSERT INTO records (datetime, programming_language, minutes_spent, rating, programmer_id, description) VALUES (%s, %s, %s, %s, %s, %s)', ['2022-12-28 17:05:11', 'python', 20, 3, 2, 'Ahoj']), 'post querry is wrong'
assert instance2.generate_insert_query() == ('INSERT INTO records (datetime, programming_language, minutes_spent, rating, programmer_id, description) VALUES (%s, %s, %s, %s, %s, %s)', ['2022-12-28 17:05:11', 'python', 20, 3, 2, 'Ahoj']), 'ID query is wrong'
assert instance3.generate_insert_query().value_name == 'datetime', 'datetime query is wrong'
assert instance4.generate_insert_query().value_name == 'programming_language', 'programming_languagequery is wrong'
assert instance5.generate_insert_query().value_name == 'rating', 'rating query is wrong'
assert instance6.generate_insert_query() == ('INSERT INTO records (datetime, programming_language, minutes_spent, rating, description) VALUES (%s, %s, %s, %s, %s)', ['2022-12-28 17:05:11', 'python', 20, 3, 'Ahoj']), 'programmer_id query is wrong'
assert instance7.generate_insert_query() == ('INSERT INTO records (datetime, programming_language, minutes_spent, rating, programmer_id) VALUES (%s, %s, %s, %s, %s)', ['2022-12-28 17:05:11', 'python', 20, 3, 2]), 'description query is wrong'


# -------- testing put --------
try:
    instance1.generate_update_query()
except EmptyRequest:
    pass
else:
    print('Empty exception failed.')
instance1.update_value(DATE, '2023-01-01 03:20:52')
assert instance1.generate_update_query() == ('UPDATE records SET datetime = %s WHERE id = %s', ['2023-01-01 03:20:52', 96]), 'update querry'

instance1.update_value(PROGRAMMING_LANGUAGE, 'python')
assert instance1.generate_update_query() == ('UPDATE records SET datetime = %s,  programming_language = %s WHERE id = %s', ['2023-01-01 03:20:52', 'python', 96]), 'update querry'

instance1.update_value(TIME_SPENT, 60)
assert instance1.generate_update_query() == ('UPDATE records SET datetime = %s,  programming_language = %s,  minutes_spent = %s WHERE id = %s', ['2023-01-01 03:20:52', 'python', 60, 96]), 'update querry'

instance1.update_value(RATING, 5)
assert instance1.generate_update_query() == ('UPDATE records SET datetime = %s,  programming_language = %s,  minutes_spent = %s,  rating = %s WHERE id = %s', ['2023-01-01 03:20:52', 'python', 60, 5, 96]), 'update querry'

instance1.update_value(PROGRAMMER_ID, 3)
assert instance1.generate_update_query() == ('UPDATE records SET datetime = %s,  programming_language = %s,  minutes_spent = %s,  rating = %s,  programmer_id = %s WHERE id = %s', ['2023-01-01 03:20:52', 'python', 60, 5, 3, 96]), 'update querry'

instance1.update_value(PROGRAMMER_ID, None)
assert instance1.generate_update_query() == ('UPDATE records SET datetime = %s,  programming_language = %s,  minutes_spent = %s,  rating = %s,  programmer_id = %s WHERE id = %s', ['2023-01-01 03:20:52', 'python', 60, 5, None, 96]), 'update querry'

instance1.update_value(DESCRIPTION, 'updated')
instance1.update_value(PROGRAMMER_ID, 3)
assert instance1.generate_update_query() == ('UPDATE records SET datetime = %s,  programming_language = %s,  minutes_spent = %s,  rating = %s,  programmer_id = %s,  description = %s WHERE id = %s', ['2023-01-01 03:20:52', 'python', 60, 5, 3, 'updated', 96]), 'update query'

# query, values = instance1.generate_put_query()
# print(query)
# mycursor.execute(query, values)
# mycursor.execute(get_query)
# print(mycursor.fetchall())


# -------- testing delete --------
assert instance1.generate_delete_query() == ('DELETE FROM records WHERE id = %s;', [96]), instance1.generate_delete_query()


# -------- test record to str --------

assert str(instance1) == '{"id": 96, "datetime": "2023-01-01 03:20:52", "programming_language": "python", "minutes_spent": 60, "rating": 5, "programmer_id": 3, "description": "updated"}', 'Error in converting record to string.'
assert str(instance2) == '{"id": null, "datetime": "2022-12-28 17:05:11", "programming_language": "python", "minutes_spent": 20, "rating": 3, "programmer_id": 2, "description": "Ahoj"}', 'Error in converting record to string.'
assert str(instance3) == '{"id": 0, "datetime": null, "programming_language": "python", "minutes_spent": 20, "rating": 3, "programmer_id": 2, "description": "Ahoj"}', 'Error in converting record to string.'
assert str(instance4) == '{"id": 0, "datetime": "2022-12-28 17:05:11", "programming_language": null, "minutes_spent": 20, "rating": 3, "programmer_id": 2, "description": "Ahoj"}', 'Error in converting record to string.'
assert str(instance5) == '{"id": 0, "datetime": "2022-12-28 17:05:11", "programming_language": "python", "minutes_spent": 20, "rating": null, "programmer_id": 2, "description": "Ahoj"}', 'Error in converting record to string.'
assert str(instance6) == '{"id": 0, "datetime": "2022-12-28 17:05:11", "programming_language": "python", "minutes_spent": 20, "rating": 3, "programmer_id": null, "description": "Ahoj"}', 'Error in converting record to string.'
assert str(instance7) == '{"id": 0, "datetime": "2022-12-28 17:05:11", "programming_language": "python", "minutes_spent": 20, "rating": 3, "programmer_id": 2, "description": null}', 'Error in converting record to string.'

# -------- test if all obligatory arguments passed --------
assert instance1.check_if_all_obligatory_values_provided() == True, 'Error in obligatory values check.'
assert instance2.check_if_all_obligatory_values_provided() == False, 'Error in obligatory values check.'
assert instance3.check_if_all_obligatory_values_provided() == False, 'Error in obligatory values check.'
assert instance4.check_if_all_obligatory_values_provided() == False, 'Error in obligatory values check.'
assert instance5.check_if_all_obligatory_values_provided() == False, 'Error in obligatory values check.'
assert instance6.check_if_all_obligatory_values_provided() == True, 'Error in obligatory values check.'
assert instance7.check_if_all_obligatory_values_provided() == True, 'Error in obligatory values check.'
