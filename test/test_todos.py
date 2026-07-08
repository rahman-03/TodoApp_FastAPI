from fastapi import status
from app.auth.dependencies import get_db, get_current_user
from app.models.todo import Todos
from .utils import *

# test get all todos
def test_read_all_authenticated(user_override, insert_test_user, insert_test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'title': 'EAT',
        'description': 'breakfast',
        'priority': 5,
        'complete': False,
        'owner_id': insert_test_todo.owner_id,
        'id': insert_test_todo.id
    }]

# test get todo by id
def test_read_one_authenticated(user_override, insert_test_user, insert_test_todo):
    response = client.get(f'/todos/{insert_test_todo.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'title': 'EAT',
        'description': 'breakfast',
        'priority': 5,
        'complete': False,
        'owner_id': insert_test_todo.owner_id,
        'id': insert_test_todo.id
    }

# test not found get todo by id
def test_read_one_authenticated_not_found(user_override, insert_test_user, insert_test_todo):
    response = client.get(f'/todos/{insert_test_todo.id + 1}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail' : 'Todo not found'
    }


# Test Create a todo
def test_create_todo(user_override, insert_test_user):
    req_data = {
        'title': 'Walk',
        'description': '2km',
        'priority': 5,
        'complete': False,
    }
    response = client.post("/todos", json=req_data)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["title"] == req_data["title"]
    assert data["description"] == req_data["description"]
    assert data["priority"] == req_data["priority"]
    assert data["complete"] == req_data["complete"]
    assert data["owner_id"] == insert_test_user.id

# test update a todo
def test_update_todo(user_override, insert_test_user, insert_test_todo):
    req_data = {
        'title': 'Walk',
        'description': '2km',
        'priority': 5,
        'complete': False,
    }
    response = client.put(f'/todos/{insert_test_todo.id}',json=req_data)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["title"] == req_data["title"]
    assert data["description"] == req_data["description"]
    assert data["priority"] == req_data["priority"]
    assert data["complete"] == req_data["complete"]

# test not found update a todo
def test_update_todo_not_found(user_override, insert_test_user, insert_test_todo):
    req_data = {
        'title': 'Walk',
        'description': '2km',
        'priority': 5,
        'complete': False,
    }
    response = client.put(f'/todos/{insert_test_todo.id + 1}',json=req_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail' : 'Item not found'
    }

# test delete todo
def test_delete_todo(user_override, insert_test_user, insert_test_todo):
    response = client.delete(f'/todos/{insert_test_todo.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db =TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == insert_test_todo.id).first()
    assert not model

# test not found delete todo
def test_delete_todo_not_found(user_override, insert_test_user, insert_test_todo):
    response = client.delete(f'/todos/{insert_test_todo.id + 1}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail' : 'Item not found'
    }