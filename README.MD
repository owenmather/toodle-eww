#### :notebook: Toodle-eww
A basic todo server hosted on AWS Lambda with state management using this Github Repo


### :anchor: Endpoints 
REST API Endpoints exposed by the backend

```bash
/todos: GET - List All Todos
/todos/:id: GET - Get Todo by ID
/todos: POST - Create Todo
/todos/:id: PUT - Update Todo
/todos/:id: DELETE - Delete Todo
```


### :flags: Environment Variables
Environment Variables exposed by the backend


| Variable | Value | Description |
| -------- | ----- | ----- |
| `GITHUB_REPO` | `postgres://user:pass@host:port/database` | URL to Github Repo |
| `GITHUB_TOKEN` | `secret` | Token for GitHub Auth |
| `BRANCH` | `master` | branch file is located in |
| `TODO_PATH` | `data/todo.csv` | Path to CSV file in repo |