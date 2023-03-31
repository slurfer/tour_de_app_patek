from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable





TABLE = 'note'

class Note(DatabaseTable):
    TABLE_NAME: str = 'notes'
    VALUE_INFO: Dict[str, Value] = {
            ID: Value(ID, int, True, primary_key=True, editable=False),
            AUTHOR: Value(AUTHOR, str, True),
            CONTENT: Value(CONTENT, str, True),
            COLOR: Value(COLOR, str, True),
    }
    FOREIGN_KEYS: List[Tuple[str, str]] = None


    def __init__(
        self,
        id: int = None,
        author: str = None,
        content: str = None,
        color: str = None,
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
                author,
                content,
                color,
            ), ignore_values_with_not_store_flag=True
            )
    
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Note.TABLE_NAME};'
    

            
    

        
    
    


