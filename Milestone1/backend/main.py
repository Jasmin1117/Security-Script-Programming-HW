from flask import Flask, request, jsonify
from validation import validate_name, validate_email, validate_age, validate_password, sanitize_input,  hash_password

app = Flask(__name__)

@app.route('/form', methods=['POST'])
def validate_form():
    data = request.json or {}  # Get JSON data from request
    
    errors = {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    age = data.get("age")
    password = data.get("password").strip()
    message = data.get("message", "").strip()

    validate_name(name, errors)
    validate_email(email, errors)
    validate_age(age, errors)
    validate_password(password, errors)
    

    hashed_password, salt = hash_password(password)  
    sanitized_message = sanitize_input(message) 
    
    
    if errors:
        return jsonify({"errors": errors}), 400

    # Return success response with sanitized data
    return jsonify({
        "message": "Form submitted successfully!",
        "data": {
            "name": name,
            "email": email,
            "age": age,
            "password": hashed_password,
            "salt": salt.hex(),
            "message": sanitized_message
        }
    }), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)

