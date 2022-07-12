# AWS Lambda function for handling TODOs
import os
import logging

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


def lambda_handler(event):
    logger.debug(event)

    # check lambda event to check http method
    if event['httpMethod'] == 'GET':
        return get_todos()
    elif event['httpMethod'] == 'POST':
        return create_todo(event)
    elif event['httpMethod'] == 'PUT':
        return update_todo(event)
    elif event['httpMethod'] == 'DELETE':
        return delete_todo(event)
    else:
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed'
        }


def delete_todo(event):
    pass


def update_todo(event):
    pass


def create_todo(event):
    pass


def get_todos():
    pass


