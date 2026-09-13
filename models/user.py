import hashlib
import json
import os

from utils.validators import not_empty, valid_email


USERS_FILE = "data/users.json"


class User:
    def __init__(self, user_id, username, email, password_hash):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __str__(self):
        return f"{self.user_id} - {self.username}"


def load_users(filepath=USERS_FILE):
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    users = []
    for item in data:
        user = User(item["user_id"], item["username"], item["email"], item["password_hash"])
        users.append(user)
    return users


def save_users(users, filepath=USERS_FILE):
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    data = []
    for user in users:
        data.append({
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "password_hash": user.password_hash,
        })

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def generate_user_id(users):
    if not users:
        return "U001"
    number = int(users[-1].user_id.replace("U", "")) + 1
    return f"U{number:03d}"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password, filepath=USERS_FILE):
    if not not_empty(username) or not valid_email(email) or not not_empty(password):
        return False, "username, valid email and password are required"

    users = load_users(filepath)
    for user in users:
        if user.username == username:
            return False, "username already exists"

    user = User(generate_user_id(users), username.strip(), email.strip(), hash_password(password))
    users.append(user)
    save_users(users, filepath)
    return True, user


def login_user(username, password, filepath=USERS_FILE):
    if not not_empty(username) or not not_empty(password):
        return False, "username and password are required"

    users = load_users(filepath)
    password_hash = hash_password(password)
    for user in users:
        if user.username == username and user.password_hash == password_hash:
            return True, user

    return False, "invalid username or password"

