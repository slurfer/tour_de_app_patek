from typing import Dict, Tuple, List, Any
import json

class TDAException(Exception):
    """Generic TDA Exception"""
    def __init__(self) -> None:
        self.message = 'Generic server Error'
        self.code = 500

    def __str__(self) -> str:
        print(self.message)
        return json.dumps({'message': self.message})

class MissingOblitagoryValue(TDAException):
    """Missing obligatory value exception.
    Used when obligatory value is missing in request.
    Args:
        value_name (str, optional): Name of the value. Defaults to empty string.
    """

    def __init__(self, value_name = '') -> None:
        self.value_name = value_name
        self.code = 400
        self.message = f'Missing obligatory value: {self.value_name}'
    

class TryingToUpdateUnupdatableValue(TDAException):
    """Trying to update unupdatable value exception.
    Used when trying to update unupdatable value.
    Args:
        value_name (str): Name of the value.
    """
    def __init__(self, value_name: str) -> None:
        self.value_name = value_name
        self.message = f'Trying tu update to unupdatable value "{self.value_name}"'
        self.code = 400


class NonExistingKey(TDAException):
    """Non existing key exception.
    Used when trying to access non existing key from database.
    Args:
        key_name (str): Name of the key.
        key_value (str): Value of the key.
    """
    def __init__(self, key_name, key_value) -> None:
        self.code = 404
        self.message = f'Non existing key ({key_name} with value {key_value})'



class EmptyRequest(TDAException):
    """Empty request exception.
    Used when http request does not contain any data.
    """
    def __init__(self) -> None:
        self.code = 400
        self.message = f'Empty Request'



class NonExistingUser(TDAException):
    """Trying to access non existing user exception.
    Args:
        username (str): Username of the user.
    """
    def __init__(self, username) -> None:
        self.code = 401
        self.message = f'Non existing user: {username}'



class WrongCredentials(TDAException):
    """Wrong credentials exception.
    Used when user provides wrong credentials.
    Args:
        username (str): Username of the user.
    """
    def __init__(self, username) -> None:
        self.code = 401
        self.message = f'Wrong credentials for: {username}'



class WrongValueType(TDAException):
    """Wrong value type exception.
    Args:
        type_name (str): Name of the type.
    """
    def __init__(self, type_name) -> None:
        self.code = 400
        self.message = f'Wrong type: {type_name}'



class ValueAlreadyExist(TDAException):
    """Value already exist exception.
    Used when trying to add value that already exist in database. (for example username or ID)
    Args:
        value_name (str): Name of the value.
        value (any): Value.
    """
    def __init__(self, value_name, value) -> None:
        self.code = 400
        self.message = f'{value_name}: {value} is not unique'


class InvalidToken(TDAException):
    """Invalid token exception.
    used when provided token is invalid.
    """
    def __init__(self) -> None:
        self.code = 401
        self.message = f'Invalid token.'


class AccessDenied(TDAException):
    """Access denied exception.
    Used when user does not have access to requested resource.
    """
    def __init__(self) -> None:
        self.code = 401
        self.message = f'Access denied.'


class WrongFileType(TDAException):
    """Wrong file type exception.
    Used when uploaded file has unsupported type.
    Args: message (str): Message.
    """
    def __init__(self, message) -> None:
        self.code = 400
        self.message = f'WrongFileType: {message}'


class NotFound(TDAException):
    """Not found exception.
    Generic not found exception.
    NotFound is used for hiding information about raised exceptions.
    """
    def __init__(self) -> None:
        self.code = 404
        self.message = "Not found"
