import re
from bs4 import BeautifulSoup
import os
import hashlib


# Regular expression for a valid email format
EMAIL_REGEX = r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$"
  
def validate_name(name, errors):
    if not name:
        errors["name"] = "Name is required."
    elif len(name) > 50:
        errors["name"] = "Name must not exceed 50 characters."


def validate_email(email, errors):
    if not email:
        errors["email"] = "Email is required."
    elif not re.match(EMAIL_REGEX, email):
        errors["email"] = "Invalid email format."


def validate_age(age, errors):
    if age is not None:
        try:
            age = int(age)
            if age < 18 or age > 120:
                errors["age"] = "Age must be between 18 and 120."
        except ValueError:
            errors["age"] = "Age must be a number."


def validate_password(password, errors):
    # strong password
    if len(password) >= 12 and any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c.isdigit() for c in password) and re.search(r"[!@#$%^&*()\-_=+]", password):
        pass  
    # moderate password
    elif len(password) >= 8 and any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c.isdigit() for c in password):
        errors["password"] = "Password is moderate only."
    # weak password
    else:
        errors["password"] = "Password is weak."


def sanitize_input(message):
    if message:
        return BeautifulSoup(message, "html.parser").get_text().strip()
    return 


def hash_password(password):
    salt = os.urandom(16)
    hashed_password = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
    return hashed_password, salt




