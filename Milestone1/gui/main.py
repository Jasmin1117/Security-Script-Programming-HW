import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests


def submit_form():
    """Handles form submission and sends data to Flask API"""
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    age = age_entry.get().strip()
    password = password_entry.get()
    message = message_text.get("1.0", tk.END).strip()

    form_data = {
        "name": name,
        "email": email,
        "age": age if age else None,
        "password": password,
        "message": message if message else None
    }

    try:
        response = requests.post("http://127.0.0.1:5000/form", json=form_data)
        result = response.json()

        if response.status_code == 200:
            messagebox.showinfo("Success", result.get("message", "Form submitted successfully!"))
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Name: {name}\n")
            result_text.insert(tk.END, f"Email: {email}\n")
            result_text.insert(tk.END, f"Age: {age if age else 'N/A'}\n")
            result_text.insert(tk.END, f"Message: {message}\n")
        else:
            error_msg = "\n".join([f"{key}: {value}" for key, value in result.get("errors", {}).items()])
            messagebox.showerror("Error", f"Validation failed:\n{error_msg}")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Connection Error", f"Could not connect to server: {e}")


def clear_form():
    """Clears all input fields"""
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    message_text.delete("1.0", tk.END)
    result_text.delete("1.0", tk.END)


# GUI Setup
app = tk.Tk()
app.title("Web Security Tool")
app.geometry("500x600")

# Form Labels and Inputs
tk.Label(app, text="Name *", font=("Arial", 10)).pack(pady=5)
name_entry = tk.Entry(app, width=40)
name_entry.pack()

tk.Label(app, text="Email *", font=("Arial", 10)).pack(pady=5)
email_entry = tk.Entry(app, width=40)
email_entry.pack()

tk.Label(app, text="Age", font=("Arial", 10)).pack(pady=5)
age_entry = tk.Entry(app, width=40)
age_entry.pack()

tk.Label(app, text="Password", font=("Arial", 10)).pack(pady=5)
password_entry = tk.Entry(app, width=40, show="*")  # Hide password input
password_entry.pack()

tk.Label(app, text="Message", font=("Arial", 10)).pack(pady=5)
message_text = scrolledtext.ScrolledText(app, width=50, height=5)
message_text.pack()

# Submit and Clear Buttons
submit_button = tk.Button(app, text="Submit", command=submit_form, font=("Arial", 12))
submit_button.pack(pady=10)

clear_button = tk.Button(app, text="Clear", command=clear_form, font=("Arial", 12))
clear_button.pack(pady=10)  # Fixed the issue by removing row/column

# Result Section
tk.Label(app, text="Submitted Data:", font=("Arial", 10, "italic")).pack(pady=5)
result_text = scrolledtext.ScrolledText(app, width=50, height=7)
result_text.pack()

app.mainloop()
