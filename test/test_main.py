from unittest import TestCase

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    raise ImportError("dotenv is required to run the tests")

from src.main import fetch_todos, parse_todos, get_todos, create_todo, delete_todo


class Test(TestCase):

    def test_fetch_todos(self):
        todos = fetch_todos()
        with open("../data/todo.csv", "r") as f:
            local_todos = f.read()
            self.assertEqual(len(todos), len(local_todos))
            self.assertEqual(todos, local_todos)
            print(local_todos)

    def test_parse_todos(self):
        parsed = parse_todos(todos=fetch_todos())
        print(parsed)

    def test_missing_get_todos(self):
        event = {"pathParameters": {"id": "100"}, "httpMethod": "GET"}
        assert get_todos(event)["statusCode"] == 404

    def test_found_get_all_todos(self):
        event = {"httpMethod": "GET"}
        assert get_todos(event)["statusCode"] == 200

    def test_create_todo(self):
        event = {"body": "Count to infinity again,Count to infinity again,2022-11-01,true", "httpMethod": "POST"}
        assert create_todo(event)["statusCode"] == 200

    def test_get_todo_by_id(self):
        event = {"pathParameters": {"id": "2"}, "httpMethod": "GET"}
        assert get_todos(event)["statusCode"] == 200

    def test_delete_todo(self):
        event = {"pathParameters": {"id": "3"}, "httpMethod": "DELETE"}
        assert delete_todo(event)["statusCode"] == 200
