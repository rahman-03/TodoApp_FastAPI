from fastapi import status
from app.auth.dependencies import get_db, get_current_user
from .utils import *

# test get user
def test_get_user(user_override, insert_test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == insert_test_user.username
    assert response.json()['email'] == insert_test_user.email

# test change password success
def test_change_password_success(user_override, insert_test_user):
    response = client.put('/user/change_pass',json={'old_pass' : 'testpassword', 'new_pass' : 'testpass123', 'conf_pass' : 'testpass123'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message" : "Password Updated Successfully"}

# test change password incorrect oldpass
def test_change_password_incorrect_oldpass(user_override, insert_test_user):
    response = client.put('/user/change_pass',json={'old_pass' : 'incorrectpassword', 'new_pass' : 'testpass123', 'conf_pass' : 'testpass123'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail" : "Authentication Failed"}

# test change password validation mismatch
def test_change_password_validation_mismatch(user_override, insert_test_user):
    response = client.put('/user/change_pass',json={'old_pass' : 'testpassword', 'new_pass' : 'testpass123', 'conf_pass' : 'testpasswor'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail" : "Password not matched"}

# test details change
def test_details_change_success(user_override, insert_test_user):
    details = {
        'password' : 'testpassword',
        'email' : 'changedtest@samptest.com',
        'firstname' : 'changedtestfirstname',
        'lastname' : 'changedtestlastname',
        'phone_no' : '0012345670'
    }
    response = client.put('/user/details_change',json=details)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message" : "Details Updated Successfully"}
