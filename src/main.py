# AWS Lambda function for handling TODOs
import os
import logging
from typing import Dict, Union, List

import requests
import base64
import json

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

try:
    GITHUB_REPO = os.environ['GITHUB_REPO']
    GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
    BRANCH = os.environ.get('BRANCH', "master")
    TODO_PATH = os.environ.get('TODO_PATH', "data/todo.csv")
except KeyError as e:
    logging.error("Missing environment variable: {}".format(e))
    raise e


def lambda_handler(event: Dict):
    logger.debug(event)
    action = ACTIONS.get(event['httpMethod'], lambda _: response(405))
    return action(event)


def response(status_code: int, body: Union[str, int, Dict, List] = None) -> Dict:
    default_http_messages = {
        200: 'OK',
        201: 'Created',
        210: 'Deleted',
        204: 'No Content',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        405: 'Method Not Allowed',
        404: 'Not Found',
        500: 'Internal Server Error',
    }

    return {
        'statusCode': status_code,
        'body': default_http_messages[status_code] if body is None else json.dumps(body)
    }


def _save_todos(todos: List):
    #   https://api.github.com/repos/OWNER/REPO/contents/PATH \
    headers = {'Accept': 'application/vnd.github+json', 'Authorization': 'token {}'.format(GITHUB_TOKEN)}
    url = 'https://api.github.com/repos/{}/contents/{}?ref={}'.format(GITHUB_REPO, TODO_PATH, BRANCH)
    body = {"message": "saving todo update",
            "content": base64.b64encode("\n".join(todos).encode("utf-8")).decode(),
            "sha": META["sha"]}
    resp = requests.put(url=url, headers=headers, data=json.dumps(body))
    resp.raise_for_status()
    return resp.status_code


def delete_todo(event: Dict):
    todo_id = event.get('pathParameters', {}).get('id', None)
    if todo_id is None:
        return response(400, "Must specify a todo id")
    todos = parse_todos(fetch_todos())
    if _valid_id(todo_id, todos):
        todos.pop(int(todo_id) - 1)
        status = _save_todos(todos)
        return response(status)


def create_todo(event: Dict):
    todo = event.get('body', {})
    todos = parse_todos(fetch_todos())
    todos.append(todo)
    status = _save_todos(todos)
    return response(status)


def update_todo(event: Dict):
    pass


def get_todos(event: Dict) -> Dict:
    todo_id = event.get('pathParameters', {}).get('id', None)
    todos = parse_todos(fetch_todos())
    if todo_id is not None:
        return response(200, todos[int(todo_id) - 1]) if _valid_id(todo_id, todos) else response(404)
    else:
        return response(200, todos)


def _valid_id(todo_id: Union[str, int], todos: List) -> bool:
    """
    Checks if the todo id is valid. The todo_id is valid if it is a line number
    :param todo_id:
    :param todos:
    :return:
    """
    if type(todo_id) == str and not todo_id.isnumeric():
        return False
    # Line 1 is headers
    return len(todos) + 2 >= int(todo_id) > 1


def parse_todos(todos: str) -> List:
    # Parses the todos and returns a List of todos
    rows = todos.splitlines()
    return rows


def _to_json(todos: str):
    # Parses the todos and returns a dict of todos
    rows = todos.splitlines()
    # First row is always the header
    header = [row.strip() for row in rows[0].split(',')]
    result = []
    for idx, row in enumerate(rows[1:]):
        # Headers are zipped into a dict each each row as values
        todo = dict(zip(header, row.split(',')))
        todo['title'] = todo['title'].strip()
        todo['description'] = todo['description'].strip()
        todo['created_date'] = todo['created_date'].strip()
        todo['completed'] = todo['completed'].strip().lower() in TRUTH_VALUES
        # Line number in csv is used as the id
        result.append(todo)
    return rows


def fetch_todos() -> str:
    # Connects to GitHub API and fetches todos
    # Returns a list of todos
    # using https://docs.github.com/en/rest/repos/contents#get-repository-content
    headers = {'Accept': 'application/vnd.github+json'}
    url = 'https://api.github.com/repos/{}/contents/{}?ref={}'.format(GITHUB_REPO, TODO_PATH, BRANCH)
    resp = requests.get(url=url, headers=headers)
    resp.raise_for_status()
    resp_json = resp.json()
    META["sha"] = resp_json["sha"]
    return base64.b64decode(resp_json['content']).decode('utf-8')


TRUTH_VALUES = ['true', 't', '1', 'y', 'yes']
ACTIONS = {"GET": get_todos, "POST": create_todo, "PUT": update_todo, "DELETE": delete_todo}
META = {}
