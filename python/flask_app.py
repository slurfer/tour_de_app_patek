from datetime import datetime
from flask import Flask, request, abort, Request, jsonify, make_response, send_file
import flask
import json
from typing import Dict, Tuple, List, Any, Callable
from flask_cors import CORS
from data_classes.note import Note
from database_table import DatabaseTable
from constants import *
from tour_de_app_database import TourDeAppDatabase
from classes import *
from Errors import *
from functools import wraps
import jwt
from datetime import datetime, timedelta
import requests
from data_classes.commit import Commit

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

def response_to_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return json.dumps(f(*args, **kwargs))
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


def update_commits():
    sql_select = Commit.generate_select_query()
    select_response = DATABASE.select(sql_select)
    if len(select_response.data) > 0:
        last_commit = Commit(query=select_response.data[-1])
        last_commit_date = last_commit.values[DATE].value
        response = requests.get(f'{URL}/commit/filter/{last_commit_date}', headers=HEADERS)
        data = json.loads(response.text)
        data.pop(0)
    else:
        response = requests.get(f'{URL}/commit/', headers=HEADERS)
        data = json.loads(response.text)
    for commit in data:
        commit_object = Commit(
            commit_id=commit['commit_id'],
            creator_id=commit['creator_id'],
            date=commit['date'],
            lines_added=commit['lines_added'],
            lines_removed=commit['lines_removed'],
            description=commit['description'],
        )
        sql_insert, sql_insert_values = commit_object.generate_insert_query()
        print(sql_insert, sql_insert_values)
        query = DATABASE.insert(sql_insert, sql_insert_values, return_last_added=False)


def get_commits_from_database():
    update_commits()
    sql_select = Commit.generate_select_query()
    select_response = DATABASE.select(sql_select)
    data = []
    for commit in select_response.data:
        data.append(Commit(query=commit))
    return data


update_commits()

# ========================== BASICS ==========================

@app.route('/basics/uptime', methods=['GET'])
@handle_errors
@handle_response
@response_to_json
def get_uptime():
    response = requests.get(f'{URL}/sysinfo/', headers=HEADERS)
    data = json.loads(response.text)
    print(data)
    output = {}
    output['boot_time'] = data['boot_time']
    output['platform'] = data['platform']
    print(output)
    return output



@app.route('/basics/commits', methods=['GET'])
@handle_errors
@handle_response
@response_to_json
def get_commits():
    data = get_commits_from_database()
    # print(data)
    output = {}
    output['count'] = len(data)
    output['last'] = data[-1].__dict__()
    print(output)
    return output


@app.route('/monitor/info', methods=['GET'])
@handle_errors
@handle_response
@response_to_json
def get_monitor_info():
    response = requests.get(f'{URL}/sysinfo/', headers=HEADERS)
    data = json.loads(response.text)
    # print(data)
    output = {}
    output['cpu_load'] = data['cpu_load']
    output['ram_usage'] = data['ram_usage']
    output['disk_usage'] = data['disk_usage']
    print(output)
    return output



@app.route('/bacics/topProgrammer', methods=['GET'])
@handle_errors
@handle_response
@response_to_json
def get_top_programmer():
    commits = get_commits_from_database()
    programmers = {}
    for commit in commits:
        programmer_id = commit.values[CREATOR_ID].value
        if programmer_id not in programmers:
            programmers[programmer_id] = 1
        else:
            programmers[programmer_id] += 1
    top_programmer = max(programmers, key=programmers.get)
    print(top_programmer)
    output = {
        'top_programmer': top_programmer,
    }
    return output


@app.route('/longStats/commitsByDate', methods=['GET'])
@handle_errors
@handle_response
@response_to_json
def get_commits_by_date():
    commits = get_commits_from_database()
    commits_by_date = {}
    for commit in commits:
        date = commit.values[DATE].value.split('T')[0]  # Extract the date component
        if date not in commits_by_date:
            commits_by_date[date] = 1
        else:
            commits_by_date[date] += 1
    print(commits_by_date)
    # Sort the dictionary by the values in descending order
    sorted_commits_by_date = dict(sorted(commits_by_date.items(), key=lambda item: item[1], reverse=True))

    # Select only the top 10 dates with the highest number of commits
    top_10_commits_by_date = dict(list(sorted_commits_by_date.items())[:10])

    output = {
        'commits_by_date': top_10_commits_by_date,
    }
    return output





# ========================== PROGRAMMER ==========================

@app.route('/note', methods=['POST'])
@handle_errors
@handle_response
def create_note():
    data = get_data_from_request(request)
    note = Note(request = data)
    check_unigue_values(note, Note)
    sql_insert, sql_insert_values = note.generate_insert_query()
    query = DATABASE.insert(sql_insert, sql_insert_values).data[0]
    response = Note(query = query)
    print('-'*100)

    return response


@app.route('/note', methods=['GET'])
@handle_errors
@handle_response
def get_note_info():
    sql_select = Note.generate_select_query()
    select_response = DATABASE.select(sql_select)
    response = []
    for item in select_response.data:
        print(item)
        member = Note(query=item)
        response.append(member.__dict__())

    response_str = json.dumps(response, ensure_ascii=False)
    return response_str


@app.route('/note/<id>', methods=['PUT'])
@handle_errors
@handle_response
def update_note(id: str):
    DATABASE.check_if_id_exist(NOTES_DATABASE, int(id))
    data = get_data_from_request(request)
    if PASSWORD in data.keys() and data[PASSWORD] == None:
        data.pop(PASSWORD)
    note = Note(request=data, id=id)
    check_unigue_values(note, Note)
    sql_insert, sql_insert_values = note.generate_update_query()
    print(sql_insert, sql_insert_values)
    response = DATABASE.update(sql_insert, sql_insert_values)

    return response



@app.route('/note/<id>', methods=['DELETE'])
@handle_errors
@handle_response
def delete_note(id: str):
    sql_command: str = f'DELETE FROM {NOTES_DATABASE} WHERE id = ?;'
    DATABASE.check_if_id_exist(NOTES_DATABASE, int(id))
    response = DATABASE.delete(sql_command, [id])

    return response












if __name__ == '__main__':
    app.run(debug=True)
