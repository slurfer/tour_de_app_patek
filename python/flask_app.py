from datetime import datetime
from flask import Flask, request, abort, Request, jsonify, make_response, send_file
import flask
import json
from typing import Dict, Tuple, List, Any, Callable
from flask_cors import CORS
from data_classes.programmer import Programmer
from database_table import DatabaseTable
from constants import *
from tour_de_app_database import TourDeAppDatabase
from classes import *
from Errors import *
from functools import wraps
import jwt
from datetime import datetime, timedelta

DATABASE = TourDeAppDatabase()

app = Flask("My first server")
CORS(app)

app.config['SECRET_KEY'] = 'AAAAB3NzaC1yc2EAAAADAQABAAABgQC6wTKMh0D5C68Un/OTRZEZnbPQsDv/QpYCHAD9Mr0g+Et4M7ibBAEc+S/rZQZ+sGZ4167nt+6QsajTSZGToiP/FfP8ei/Q8Io5Zbn1+ejC9jxmIlM6p0qVS98qIiHZZPS3E/+pUF5jLEUEKB/AwuyyNJyt9NDTAfWC00CycIVWei0bHs/ooTmhoHgih2kIb71UK4XZ5Lw/7+bfMtqz+iNflWxWSNF70vyytKjNpGthZy8m5Ji/Tm/2YYiDdTeQ4bInvR7oVSuiFbk2VhiAL14zeaYL2RWQLOmLQgo5nvg5b1HBU6KYMdKSiPj4B2GYhf9hBu7dfT0HytsLNAOUZl932cdXSpApzz0gML3EtiorkEPXk7VmXD9AA4UsXVY2IwBwzZYhBqJutXYdDMd6zcgdvaHoFk7gyihkdlCJyMaCwZybOf3wuXXz5j6Uh37iQQ9BPB2OZzsn8juGdnlGTPLvpawcBlABnxxYnzu7LB84ool8VUZtR2zPt1Eukou/neE'


# ========================== TOOLS ==========================
def get_data_from_request(request: Request) -> Dict[str, Any]:
    """Returns data from request json as dict."""
    if isinstance(request.json, str):
        data: Dict[str, str] = json.loads(request.json)
    else:
        data: Dict[str, str] = request.json
    
    return data


def check_roreign_keys(data: Dict[str, Any], foreings_keys):
    for id_to_check in foreings_keys:
        if id_to_check[0] in data and data[id_to_check[0]] is not None:
            id = data[id_to_check[0]]
            table_name = id_to_check[1]
            if not DATABASE.check_if_id_exist(table_name, id) and not id == None:
                raise NonExistingKey(table_name, id)
    return None


def check_unigue_values(instance: DatabaseTable, base_class):
    for value_name in instance.VALUE_INFO.keys():
        if instance.values[value_name].unique:
            sql_insert, sql_insert_values = instance.filter_by_column_value(value_name, instance.values[value_name].value)
            occurencies = DATABASE.select(sql_insert, sql_insert_values).data
            if len(occurencies) > 0:
                print(get_ids_from_records(occurencies))
                if not instance.values[ID].value in get_ids_from_records(occurencies):
                    raise ValueAlreadyExist(value_name, instance.values[value_name].value)


def get_ids_from_records(data: Tuple[Any]) -> List[int]:
    result = []
    for record in data:
        print(record)
        result.append(record[0])
    return result


def handle_errors(f):
    """Check whether the request is valid and return the appropriate error if not."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (TDAException
            ) as error:
            return make_response(str(error), error.code) 
    return decorated_function

def hide_errors(f):
    """Hide all errors and return NotFound instead."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (TDAException
            ) as error:
            raise NotFound()
    return decorated_function


def handle_response(f):
    """Wraps result of function in flask response and adds Access-Control-Allow-Origin header."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        flask_response = flask.Response(str(f(*args, **kwargs)))
        flask_response.headers['Access-Control-Allow-Origin'] = '*'
        return flask_response
    return decorated_function


# decorator for verifying the JWT
def token_required(f):
    """Decorator for verifying the JWT.
    If the token is valid, the current user is added to function arguments.
    Otherwise, an InvalidToken exception is raised."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            raise InvalidToken
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            sql_insert, sql_insert_values = Programmer().filter_by_column_value(ID, data[ID])
            current_user = DATABASE.select(sql_insert, sql_insert_values).data[0]
            current_user = Programmer(query=current_user)
        except Exception as error:
            print(error)
            raise InvalidToken()
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated


def admin_privilege(f):
    """Decorator for verifying if the logged user has admin privileges."""
    @wraps(f)
    def decorated(user, *args, **kwargs):
        if not user.values[ISADMIN].value:
            raise AccessDenied
    
        return f(user, *args, **kwargs)
    
    return decorated






# ========================== PROGRAMMER ==========================

@app.route('/programmer', methods=['POST'])
@handle_errors
@handle_response
@token_required
@admin_privilege
def create_programmer(user: Programmer):
    data = get_data_from_request(request)
    programmer = Programmer(request = data)
    check_unigue_values(programmer, Programmer)
    sql_insert, sql_insert_values = programmer.generate_insert_query()
    query = DATABASE.insert(sql_insert, sql_insert_values).data[0]
    response = Programmer(query = query)
    print('-'*100)

    return response


@app.route('/programmer', methods=['GET'])
@handle_errors
@handle_response
@token_required
@admin_privilege
def get_programmer_info(user: Programmer):
    sql_select = Programmer.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        print(item)
        member = Programmer(query=item)
        response.append(member.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    return response_str


@app.route('/programmer/<id>', methods=['PUT'])
@handle_errors
@handle_response
@token_required
@admin_privilege
def update_programmer(user: Programmer, id: str):
    DATABASE.check_if_id_exist(PROGRAMMERS_DATABASE, int(id))
    data = get_data_from_request(request)
    if PASSWORD in data.keys() and data[PASSWORD] == None:
        data.pop(PASSWORD)
    programmer = Programmer(request=data, id=id)
    check_unigue_values(programmer, Programmer)
    sql_insert, sql_insert_values = programmer.generate_update_query()
    print(sql_insert, sql_insert_values)
    response = DATABASE.update(sql_insert, sql_insert_values)

    return response



@app.route('/programmer/<id>', methods=['DELETE'])
@handle_errors
@handle_response
@token_required
@admin_privilege
def delete_programmer(user: Programmer, id: str):
    sql_command: str = f'DELETE FROM {PROGRAMMERS_DATABASE} WHERE id = ?;'
    DATABASE.check_if_id_exist(PROGRAMMERS_DATABASE, int(id))
    response = DATABASE.delete(sql_command, [id])

    return response





# ========================== LOGIN ==========================


@app.route('/login', methods=['POST'])
@handle_errors
@handle_response
def login():
    """Login user and return JWT token."""
    data = get_data_from_request(request)

    # -------- check whether login and password are provided --------
    if LOGIN not in data.keys():
        raise WrongCredentials('Login not provided.')
    if PASSWORD not in data.keys():
        raise WrongCredentials('Password not provided.')
    user_identifyer = data[LOGIN]
    
    # -------- validate password --------
    password_is_valid = False
    for method in [USERNAME, EMAIL]: # try to login by username and then by email
        # check if user exists
        sql_insert, sql_insert_values = Programmer().filter_by_column_value(method, user_identifyer)
        database_programmer = DATABASE.select(sql_insert, sql_insert_values).data
        if len(database_programmer) == 0:
            # user does not exist
            continue
        # user exists - check password
        database_user = Programmer(query=database_programmer[0])

        password_is_valid = database_user.values[PASSWORD].validate_password(data[PASSWORD])
        if password_is_valid:
            break
    
    if password_is_valid:
        # user is valid - provide JWT token
        token = jwt.encode({
            ID: database_user.values[ID].value,
            'exp' : datetime.utcnow() + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        print(database_user.__dict__())
        return json.dumps({'token': token, 'user': database_user.__dict__()})
    else:
        # user is not valid - raise exception
        raise WrongCredentials(user_identifyer)





if __name__ == '__main__':
    app.run(debug=True)
