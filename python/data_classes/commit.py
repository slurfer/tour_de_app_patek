from constants import *
from abc import abstractmethod
from typing import Dict, Tuple, List, Any
from value import Value
from Errors import *
from database_table import DatabaseTable





TABLE = 'commit'

class Commit(DatabaseTable):
    TABLE_NAME: str = 'commits'
    VALUE_INFO: Dict[str, Value] = {
            COMMIT_ID: Value(COMMIT_ID, str, True),
            CREATOR_ID: Value(CREATOR_ID, str, True),
            DATE: Value(DATE, str, True),
            LINES_ADDED: Value(LINES_ADDED, str, True),
            LINES_REMOVED: Value(LINES_REMOVED, str, True),
            DESCRIPTION: Value(DESCRIPTION, str, True),
    }
    FOREIGN_KEYS: List[Tuple[str, str]] = None


    def __init__(
        self,
        commit_id: str = None,
        creator_id: str = None,
        date: str = None,
        lines_added: str = None,
        lines_removed: str = None,
        description: str = None,
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
                commit_id,
                creator_id,
                date,
                lines_added,
                lines_removed,
                description,
            ), ignore_values_with_not_store_flag=True
            )
    
        
    
    @staticmethod
    def generate_select_query() -> str:
        return f'SELECT * FROM {Commit.TABLE_NAME};'
    

            
    

        
    
    


