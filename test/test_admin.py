from fastapi import status
from app.auth.dependencies import get_db, get_current_user
from app.models.user import Users
from .utils import *

# test admin get all users
def test_admin_read_all_authenticated(admin_override, insert_admin_user):
    print(app.dependency_overrides[get_current_user])
    response = client.get('/admin/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': insert_admin_user.id,
        'email': 'admin@samptest.com',
        'username': 'testuseradmin',
        'firstname': 'testadminfirstname',
        'lastname': 'testadminlastname',
        'role': 'admin',
        'is_active': True,
        'phone_no': '1234569990'
    }]

# test admin get user by id
def test_admin_read_one_authenticated(admin_override, insert_admin_user):
    response = client.get(f'/admin/user/{insert_admin_user.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': insert_admin_user.id,
        'email': 'admin@samptest.com',
        'username': 'testuseradmin',
        'firstname': 'testadminfirstname',
        'lastname': 'testadminlastname',
        'role': 'admin',
        'is_active': True,
        'phone_no': '1234569990'
    }

# test admin not found get user by id
def test_admin_read_one_authenticated_not_found(admin_override, insert_admin_user):
    response = client.get(f'/admin/user/{insert_admin_user.id + 1}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail' : 'User not found'
    }

# test admin update user
def test_admin_update_user_success(admin_override, insert_admin_user, insert_test_user):
    req_data = {
        "username": "updateduser",
        "is_active": False,
        "role": "admin"
    }
    response = client.put(f"/admin/user_update/{insert_test_user.id}", json=req_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["id"] == insert_test_user.id
    assert data["username"] == req_data["username"]
    assert data["is_active"] == req_data["is_active"]
    assert data["role"] == req_data["role"]

    # Fields that were not updated should remain unchanged
    assert data["email"] == insert_test_user.email
    assert data["firstname"] == insert_test_user.firstname
    assert data["lastname"] == insert_test_user.lastname
    assert data["phone_no"] == insert_test_user.phone_no

# Test admin update self
def test_admin_update_user_self(admin_override, insert_admin_user):
    req_data = {
        'username': 'updateduser',
        'is_active': False,
        'role': 'user'
    }
    response = client.put(f'/admin/user_update/{insert_admin_user.id}',json=req_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert response.json() == {
        'detail' : 'Restricted to Update own account'
    }

# test admin not found update a user
def test_admin_update_user_not_found(admin_override, insert_admin_user):
    req_data = {
        'username': 'updateduser',
        'is_active': False,
        'role': 'user'
    }
    response = client.put(f'/admin/user_update/{insert_admin_user.id + 1}',json=req_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail' : 'User not found'
    }

# test admin delete self
def test_admin_delete_user_self(admin_override, insert_admin_user):
    response = client.delete(f'/admin/user/{insert_admin_user.id}')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        'detail' : 'Restricted to delete own account'
    }

# test admin not found delete user
def test_admin_delete_user_not_found(admin_override, insert_admin_user):
    response = client.delete(f'/admin/user/{insert_admin_user.id + 1}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail' : 'Item not found'
    }