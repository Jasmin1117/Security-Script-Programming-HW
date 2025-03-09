from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup
import re
import datetime
import hashlib
import os
import random
import string

app = Flask(__name__)

def check_pass_strength(password):
    special_char = r"[!@#$%^&*()\-_+=~\[\]{}|;:'<>,.?/]"
    if len(password) > 11 and \
            any(c.islower() for c in password) and \
            any(c.isupper() for c in password) and \
            any(c.isdigit() for c in password) and \
            re.search(special_char, password):
        return "Strong"
    elif len(password) > 8 and \
            any(c.islower() for c in password) and \
            any(c.isupper() for c in password) and \
            ((any(c.isdigit() for c in password) and \
              not re.search(special_char, password)) or \
             (not any(c.isdigit() for c in password) and \
              re.search(special_char, password))):
        return "Moderate"
    else:
        return "Weak"

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirmpass = request.form.get("repassword")
    birthday = request.form.get("birthday")
    age = request.form.get("age")
    bio = request.form.get("bio")

    form_data = {
        'name': name,
        'email': email,
        'birthday': birthday,
        'age': age,
        'bio': bio
    }

    email_pattern = r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$"

    if not name or len(name) < 2 or len(name) > 50:
        return jsonify({'error': "Please ensure that the name is filled in correctly.", **form_data})

    if not email or not re.match(email_pattern, email):
        return jsonify({'error': "Please input a valid email", **form_data})

    if not birthday:
        return jsonify({'error': "Please input your birthday (mm-dd-YYYY)", **form_data})

    if not age:
        return jsonify({'error': "Please input your age", **form_data})

    try:
        if birthday:
            birthday_date = datetime.datetime.strptime(birthday, "%m-%d-%Y")
            today = datetime.datetime.today()
            calcage = today.year - birthday_date.year
            age = int(age)
            if (today.month, today.day) < (birthday_date.month, birthday_date.day):
                calcage -= 1
            if calcage < 0 or calcage > 120:
                return jsonify({'error': "Please check if inputted year is correct", **form_data})
            if age != calcage:
                return jsonify({'error': "Birthday and age does not match", **form_data})
            if age < 18:
                return jsonify({'error': "Age can not be below 18 years old", **form_data})
        else:
            return jsonify({'error': "Please input your birthday (mm-dd-YYYY)", **form_data})

    except ValueError:
        return jsonify({'error': "Please input your birthday in the correct format: mm-dd-YYYY", **form_data})

    if not password:
        return jsonify({'error': "Password field cannot be empty.", **form_data})

    if not confirmpass:
        return jsonify({'error': "Please confirm password.", **form_data})

    if password != confirmpass:
        return jsonify({'error': "Password does not match with confirmation password.", **form_data})

    if bio:
        try:
            extract = BeautifulSoup(bio, 'html.parser')
            bio = extract.get_text(separator="\n", strip=True)
        except Exception as e:
            return jsonify({'error': f"Failed to sanitize and extract content in bio. {e}", **form_data})

    password_strength = check_pass_strength(password)

    if password_strength == "Weak":
        return jsonify({'error': "Password is too weak. Please use a stronger password.", **form_data})

    salt = os.urandom(16)
    hashed_password = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open("accounts.txt", "a") as file:
            file.write(
                f"Timestamp:{timestamp} Name:{name} Email:{email} Birthday: {birthday} Age: {age} Salt:{salt.hex()} Password: {hashed_password}\nBio: {bio}\n\n")

        return jsonify({'success': True,
                        'message': f"Account is being saved.\nName: {name}\nEmail: {email}\nBirthday: {birthday}\nAge: {age}\nSalt: {salt.hex()}\nBio: {bio}",
                        'bio': bio})

    except Exception as e:
        return jsonify({'error': f"An error occurred writing to the file. {e}", **form_data})

def generate_random_password(length=12):
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special_chars = string.punctuation

    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special_chars)
    ]

    all_chars = uppercase + lowercase + digits + special_chars
    remaining_length = length - len(password)
    for _ in range(remaining_length):
        password.append(random.choice(all_chars))

    random.shuffle(password)
    password = ''.join(password)
    return password

@app.route('/generate_password', methods=['GET'])
def generate_password_route():
    length = request.args.get('length', 12, type=int)
    password = generate_random_password(length)
    return jsonify({'password': password})

if __name__ == "__main__":
    app.run(port=5000, debug=True)