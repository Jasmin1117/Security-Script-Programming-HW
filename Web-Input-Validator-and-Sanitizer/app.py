import tkinter as tk
from tkinter import messagebox
import re
import html


# checks name and email if empty
def validate_required_fields(name, email):
    if not name:
        return "Name cannot be empty."
    if not email:
        return "Email cannot be empty."
    return None

# checks name must be letter only
def validate_name(name):
    pattern = r"^[a-zA-Z\s]+$"  # Regex for letters and spaces only
    if not re.match(pattern, name):
        return "Name can only contain letters and spaces."
    return None

def validate_email(email):
    pattern = r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$"

    if not re.match(pattern, email):
        return "Invalid email address"
    else:
        return None

# checks age between 18 and 120
def validate_age(age):
    if age:
        try:
            age = int(age)
            if not (18 <= age <= 120):
                return "Age must be between 18 and 120."
        except ValueError:
            return "Age must be a valid integer."
    return None


# removes HTML and script tags
def sanitize_message(message):
    sanitized_message = html.escape(message)  
    return sanitized_message

# saves file
def save_to_file(data):
    with open("form_data.txt", "a") as f:
        f.write(str(data) + "\n") 

# submits correct data
def submit_form():
    name = name_entry.get()
    email = email_entry.get()
    age = age_entry.get()
    message = message_entry.get()


    error_message = validate_required_fields(name, email)
    if error_message:
        messagebox.showerror("Validation Error", error_message)
        return
    
    error_message = validate_name(name)  
    if error_message:
        messagebox.showerror("Validation Error", error_message)
        return

    error_message = validate_email(email)
    if error_message:
        messagebox.showerror("Validation Error", error_message)
        return

    error_message = validate_age(age)
    if error_message:
        messagebox.showerror("Validation Error", error_message)
        return

    sanitized_message = sanitize_message(message)

    form_data = {
        "Name" : name,
        "Email" : email,
        "Age" : age,
        "Message" : sanitized_message,
    }

    save_to_file(form_data)
    messagebox.showinfo("Form Submitted", "Thank you! Your form has been successfully submitted.")
    
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    message_entry.delete(0, tk.END)


# Create the Tkinter window
root = tk.Tk()
root.title("Faretail Form Submission")

font_style = ("Arial", 16)

# Form Labels and Entry Fields
tk.Label(root, text="Name:", font=font_style).grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root, font=font_style, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Email:", font=font_style).grid(row=1, column=0, padx=10, pady=5)
email_entry = tk.Entry(root, font=font_style, width=30)
email_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Age:", font=font_style).grid(row=2, column=0, padx=10, pady=5)
age_entry = tk.Entry(root, font=font_style, width=30)
age_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Message:", font=font_style).grid(row=3, column=0, padx=10, pady=5)
message_entry = tk.Entry(root, font=font_style, width=30)
message_entry.grid(row=3, column=1, padx=10, pady=5)

# Submit Button
submit_button = tk.Button(root, text="Submit", font=font_style, command=submit_form, width=15, height=1)
submit_button.grid(row=4, columnspan=2, pady=10)

root.mainloop()





