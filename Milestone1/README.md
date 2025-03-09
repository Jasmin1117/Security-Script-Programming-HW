# User Registration Form Validation

This project ensures secure and accurate user registration by validating form fields before submission. It provides real-time feedback and displays errors using Bootstrap modals to enhance the user experience.

Validation Error Example:
https://www.loom.com/share/2bf949ac75464d36bde436c6ae636d84?sid=881767a1-d745-4bdf-a188-356b0258b2df

Validation Success Example
https://www.loom.com/share/1ad8d7bd273c4420a0760f027729dfbf?sid=0edce3f3-d036-4a93-8e4a-65300e5a720f

## Validation Rules

**Name**

* Must not be empty.
* Length should be between 2 to 50 characters.

**Email**

* Must follow a valid email format using regex.
* Example pattern: `/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/`.

**Birthday & Age**

* Birthday field cannot be empty.
* Must be in the correct format (YYYY-MM-DD).
* Age is calculated based on the birthday and must be between 18 - 120 years old.

**Password**

* Cannot be empty.
* Must be at least 12 characters long.
* Must contain at least:
    * One special character (!@#$%^&*).
    * One number (0-9).
    * One uppercase letter (A-Z).
    * One lowercase letter (a-z).
* The password confirmation field must match the original password.
* Password strength is validated:
    * Weak passwords will trigger an error.
    * Strong passwords pass validation.

**Security Features**

* Passwords are hashed and salted before being stored to enhance security.
* Users can generate a strong password using a built-in password generator.
* Bio field is sanitized to prevent XSS (Cross-Site Scripting) attacks.

## How It Works

1.  The user fills out the form.
2.  JavaScript checks for basic client-side validation.
3.  Data is sent to Flask (`app.py`) for server-side validation.
4.  If there’s an error, the error modal appears with a message.
5.  If everything is correct, the success modal appears.
6.  Passwords are hashed and stored securely.
