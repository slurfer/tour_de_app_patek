from typing import Dict, Tuple, List, Any
import json

class SelectQueryResponse:
    def __init__(self, data: List[Any]) -> None:
        self.data = data


class Query:
    def __init__(self, data) -> None:
        self.data = data


class DatabaseOperationResult:
    def __init__(self, message: str = 'Successful operation', code: int = 200, data: Any = None) -> None:
        self.message = message
        self.data = data
    

    def __str__(self) -> str:
        print(self.message)
        return json.dumps({'message': self.message})