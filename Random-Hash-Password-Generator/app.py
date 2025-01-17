import tkinter as tk
import hashlib
import os
import random
import string
from datetime import datetime
from tkinter import messagebox


# Generates a random password with at least one uppercase, one lowercase, one digit, and one special character.
def generate_random_password():
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special_chars = string.punctuation

    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(lowercase),
        random.choice(special_chars)
    ]

    all_chars = uppercase + lowercase + digits + special_chars
    remaining_length = random.randint(4, 12)
    for _ in range (remaining_length):
        password.append(random.choice(all_chars))

    random.shuffle(password)
    return ''.join(password)


# Hashes the password with a random salt and returns the hash and the salt.
def hash_password(password):
    salt = os.urandom(16)
    hashed_password = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
    return hashed_password, salt


# Saves the hashed password and salt to a file.
def save_to_file(hashed_password, salt):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open("password.txt","a") as file:
            file.write(f"Timestamp:{timestamp} Salt:{salt.hex()} Hashed: {hashed_password}\n")
        messagebox.showinfo("Password Saved", "The password has been saved to 'password.txt")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Generates a password, hashes it, and saves the hash and salt to a file.
def hash_and_save_password():
    password = generate_random_password()
    entry_field.delete(0, tk.END) 
    entry_field.insert(0, password)

    try:
        hashed_password, salt = hash_password(password)
        save_to_file(hashed_password, salt)
    except Exception as e:
         messagebox.showerror("Error", f"An error occurred while hashing the password: {str(e)}")


# Toggles the visibility of the password in the entry field.
def toggle_password_visibility():
    if entry_field.cget("show") == "*":
        entry_field.config(show="") 
        show_button.config(text="Hide")
    else:
        entry_field.config(show="*")  
        show_button.config(text="Show")


root = tk.Tk()
root.title("Random Password Generator")

label = tk.Label(root, text="Click the button to generate a random password.", font=("Arial", 14))
label.pack(pady=10)

entry_field = tk.Entry(root, width=30, show="*")
entry_field.pack(pady=5)

show_button = tk.Button(root, text="Show", command=toggle_password_visibility, font=("Arial", 14))
show_button.pack(pady=5)

generate_button = tk.Button(root, text="Generate Random Password", command=hash_and_save_password, font=("Arial", 14))
generate_button.pack(pady=20)

root.mainloop()