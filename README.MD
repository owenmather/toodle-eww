#### :notebook: Toodle-eww
A basic todo server hosted on AWS Lambda with state management using this Github Repo  

The API updates the list of todos at [data/todo.csv](data/todo.csv)

### :hammer: Testing
```bash
pip install requirements.txt
python test/test_main.py
```

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
Environment Variables used by the backend


| Variable | Value | Description |
| -------- | ----- | ----- |
| `GITHUB_REPO` | `owenmather/toodle-eww` | ${OWNER}/${REPO} for Github Repo housing csv |
| `GITHUB_TOKEN` | `secret` | Token for GitHub Auth |
| `BRANCH` | `master` | branch file is located in |
| `TODO_PATH` | `data/todo.csv` | Path to CSV file in repo |