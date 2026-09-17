def not_empty(value):
    return isinstance(value, str) and bool(value.strip())


def valid_email(email):
    if not isinstance(email, str):
        return False
    email = email.strip()
    return "@" in email and "." in email.split("@")[-1]
