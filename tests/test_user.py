import pytest

from models.user import register_user, login_user, load_users


@pytest.fixture
def user_file(tmp_path):
    return str(tmp_path / "users.json")


def test_register_and_login_user(user_file):
    ok, user = register_user("student1", "student@example.com", "secret123", user_file)
    assert ok is True
    assert user.user_id == "U001"

    users = load_users(user_file)
    assert len(users) == 1

    ok, logged = login_user("student1", "secret123", user_file)
    assert ok is True
    assert logged.username == "student1"
    assert logged.role == "user"


def test_registration_cannot_assign_admin_role(user_file):
    ok, user = register_user("student2", "student2@example.com", "secret123", user_file)
    assert ok is True
    assert user.role == "user"

