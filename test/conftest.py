import pytest
from app.main import app
from app.auth.dependencies import get_db, get_current_user
from .utils import (
    override_get_db,
    override_get_current_user,
    override_get_current_admin,
)

@pytest.fixture
def user_override():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def admin_override():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_admin
    yield
    app.dependency_overrides.clear()