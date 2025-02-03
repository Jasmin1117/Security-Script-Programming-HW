import re
import tkinter as tk
from tkinter import messagebox

def check_password():
    password = entry.get()
    reasons = []

    # Weak Password checks
    if len(password) < 8:
        strength = "Weak"
        reasons.append("Password must be at least 8 characters long.")
    elif not any(c.islower() for c in password):
        strength = "Weak"
        reasons.append("Password must have at least one lowercase letter.")
    elif not any(c.isupper() for c in password):
        strength = "Weak"
        reasons.append("Password must have at least one uppercase letter.")
    elif not any(c.isdigit() for c in password):
        strength = "Weak"
        reasons.append("Password must have at least one digit.")
    else:
        
    # Moderate Password check
        if 8 <= len(password) < 12:
            strength = "Moderate"
            reasons.append("Password is moderate.")
            
        # Strong Password check
        elif len(password) >= 12:
            if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                re.search(r'\d', password) and
                re.search(r'[^a-zA-Z0-9\s]', password)):
                strength = "Strong"
                reasons.append("Password is strong.")
            else:
                strength = "Moderate"
                reasons.append("Password must include a special character.")

    # Display result
    result_label.config(text=f"Strength: {strength}", fg="red" if strength == "Weak" else "orange" if strength == "Moderate" else "green")
    messagebox.showinfo("Password Strength", "\n".join(reasons))


root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x250")

font_style = ("Arial", 16)

# Configure grid to center widgets
root.grid_columnconfigure(0, weight=1, minsize=100)
root.grid_columnconfigure(1, weight=2, minsize=200)
root.grid_columnconfigure(2, weight=1, minsize=100)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Entry widget for password input
tk.Label(root, text="Enter a Password", font=font_style).grid(row=0, column=1, pady=(20, 5))  
entry = tk.Entry(root, show="*")
entry.grid(row=1, column=1, padx=20, pady=(5, 20))

# Button to check the password
check_button = tk.Button(root, text="Check Password", command=check_password)
check_button.grid(row=2, column=1, pady=(10, 20))

# Result label
result_label = tk.Label(root, text="", font=font_style)
result_label.grid(row=3, column=0, columnspan=3, pady=(10, 20))

# Run the application
root.mainloop()