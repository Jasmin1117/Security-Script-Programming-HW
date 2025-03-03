from flask import Flask, request, jsonify
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

# Regular expression for a valid email format
EMAIL_REGEX = r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$"

@app.route('/form', methods=['POST'])
def validate_form():
    data = request.json  # Get JSON data from request
    
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    age = data.get("age")
    message = data.get("message", "")

    errors = {}

    # Validate name
    if not name:
        errors["name"] = "Name is required."
    elif len(name) > 50:
        errors["name"] = "Name must not exceed 50 characters."

    # Validate email
    if not email:
        errors["email"] = "Email is required."
    elif not re.match(EMAIL_REGEX, email):
        errors["email"] = "Invalid email format."

    # Validate age 
    if age:
        try:
            age = int(age)
            if age < 18 or age > 120:
                errors["age"] = "Age must be between 18 and 120."
        except ValueError:
            errors["age"] = "Age must be a number."

    # Sanitize message (remove HTML tags)
    if message:
        message = BeautifulSoup(message, "html.parser").get_text()

    # If errors exist, return them
    if errors:
        return jsonify({"errors": errors}), 400

    # Return success response with sanitized data
    return jsonify({
        "message": "Form submitted successfully!",
        "data": {
            "name": name,
            "email": email,
            "age": age,
            "message": message
        }
    }), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
