from dataclasses import dataclass
from typing import Any, Callable
from Errors import *
from werkzeug.security import generate_password_hash, check_password_hash
import re

def default_value_check(value):
    return value

@dataclass
class Value:
    def __init__(
        self,
        name: str,
        type: Any,
        is_obligatory: bool,
        value = None,
        not_provided_error_statement: str = 'Value not provided',
        primary_key: bool = False,
        updated: bool = False,
        editable: bool = True,
        is_metadata: bool = False,
        do_store: bool = True,
        is_encrypted: bool = False,
        private: bool = False,
        unique: bool = False,
        force_type_update: bool = False,
        value_check: Callable = default_value_check,
        include_in_public_api: bool = True,
        public_api_name: str = None,
        public_api_type: Any = None
    ) -> None:
        self.name: str = name
        self.type: Any = type
        self.is_obligatory: bool = is_obligatory
        self._value = value
        self.not_provided_error_statement: str = not_provided_error_statement
        self.primary_key: bool = primary_key
        self.updated: bool = updated
        self.editable: bool = editable
        self.is_metadata: bool = is_metadata
        self.do_store: bool = do_store
        self.is_ensrypted: bool = is_encrypted
        self.private: bool = private
        self.unique: bool = unique
        self.force_type_update: bool = force_type_update
        self.value_check = value_check
        self.include_in_public_api: bool = include_in_public_api
        if public_api_name == None:
            self.public_api_name: str = name
        else:
            self.public_api_name: str = public_api_name
        
        if public_api_type == None:
            self.public_api_type = type
        else:
            self.public_api_type = public_api_type
        

    # -------- set property - value --------
    @property
    def value(self) -> Any:
        return self._value
    
    @value.setter
    def value(self, value: Any) -> None:
        if self.editable:
            self.set_value(value)
        else:
            raise TryingToUpdateUnupdatableValue(self.name)
    
    def force_update(self, value: Any, set_updated = False) -> None:
        self.set_value(value, set_updated)
    
    def set_value(self, value: Any, set_updated = True) -> None:
        if not value==None:
            self._value = self.value_check(self.encrypt(value))
        else:
            self._value = value
        if set_updated:
            self.updated = True
        self.check_value_type()



    def validate_password(self, value_to_check: str):
        return check_password_hash(self._value, value_to_check)
    

    def encrypt(self, new_value):
        if self.is_ensrypted:
            if re.search(r'^sha256\$', new_value) == None:
                return generate_password_hash(new_value, 'sha256')
        return new_value

    
    def check_value_type(self):
        if self._value is not None:
            try:
                self._value = self.type(self._value)
            except ValueError:
                raise WrongValueType(self.name)
    
    def touch(self):
        self.updated = True

    
    def __str__(self) -> str:
        return f"Value: {{'name':{self.name}, 'value': {self.value}}}"

