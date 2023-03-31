from record import Record
from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable
from tour_de_app_database import TourDeAppDatabase


instance1 = Record(id=124, datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, rating=3, programmer_id=2, description='Ahoj')
instance2 = Record(datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, rating=3, programmer_id=2, description='Ahoj')
instance3 = Record(id=0, programming_language='python', minutes_spent=20, rating=3, programmer_id=2, description='Ahoj')
instance4 = Record(id=0, datetime="2022-12-28 17:05:11", minutes_spent=20, rating=3, programmer_id=2, description='Ahoj')
instance5 = Record(id=0, datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, programmer_id=2, description='Ahoj')
instance6 = Record(id=0, datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, rating=3, description='Ahoj')
instance7 = Record(id=0, datetime="2022-12-28 17:05:11", programming_language='python', minutes_spent=20, rating=3, programmer_id=2)


database = TourDeAppDatabase()

select_query = instance1.generate_select_query()
insert_query, insert_query_values = instance1.generate_insert_query()
instance1.update_value(PROGRAMMING_LANGUAGE, 'javascript')
update_query, update_query_values = instance1.generate_update_query()
delete_query, delete_query_values = instance1.generate_delete_query()

print(10*'=' + 'SELECT QUERY' + 10*'=')
print(select_query)
records_array = database.select(select_query)
# records = list(map(str, records_array))
print(records_array)
print()
print(10*'=' + 'INSERT QUERY' + 10*'=')
print(insert_query)
print(database.insert(insert_query, insert_query_values, commit=False))
print()
print(10*'=' + 'UPDATE QUERY' + 10*'=')
print(update_query)
print(update_query_values)
print(database.update(update_query, update_query_values, commit=False))
print()
print(10*'=' + 'DELETE QUERY' + 10*'=')
print(delete_query)
print(delete_query_values)
print(database.delete(delete_query, delete_query_values, commit=False))