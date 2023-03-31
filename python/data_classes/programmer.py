from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable





TABLE = 'programmers'

class Programmer(DatabaseTable):
    TABLE_NAME: str = 'programmers'
    VALUE_INFO: Dict[str, Value] = {
            ID: Value(ID, int, True, primary_key=True, editable=False),
            NAME: Value(NAME, str, True),
            SURNAME: Value(SURNAME, str, True),
            USERNAME: Value(USERNAME, str, True, unique=True),
            EMAIL: Value(EMAIL, str, True, unique=True),
            PASSWORD: Value(PASSWORD, str, True, is_encrypted=True, private=True),
            ISADMIN: Value(ISADMIN, bool, True),
    }
    FOREIGN_KEYS: List[Tuple[str, str]] = None


    def __init__(
        self,
        id: int = None,
        name: str = None,
        surname: str = None,
        username: str = None,
        email: str = None,
        password: str = None,
        is_admin: bool = None,
        query: str = None,
        request: Dict[str, Any] = None
    ) -> None:
        # -------- values --------
        if not query == None:
            self.init_from_tuple(query)
        elif not request == None:
            self.init_from_request(request, id)
        else:
            self.init_from_tuple((
                id,
                name,
                surname,
                username,
                email,
                password,
                is_admin
            ), ignore_values_with_not_store_flag=True
            )
    
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Programmer.TABLE_NAME};'
    

            
    

        
    
    


