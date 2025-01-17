import re
import tkinter as tk
from tkinter import messagebox


def check_password():
    try:
        password = entry.get()
        passwordlength = len(password)

        # weak password 
        if passwordlength < 8:
            if (any(c.islower() for c in password) or
                any(c.isupper() for c in password)):
                messagebox.showinfo("Weak Password", "Your password is weak")
                
        # moderate password
        elif passwordlength >= 8 and passwordlength < 12:
            if (any(c.islower()for c in password)  and
                any(c.isupper() for c in password) and
                re.search(r'\d', password)):
                messagebox.showinfo("Moderate Password", "Your password is moderate")
                return
            
        # strong password
        elif passwordlength >= 12:
            if (any(c.islower() for c in password)  and
                any(c.isupper() for c in password) and
                re.search(r'\d', password) and
                re.search(r'[^a-zA-Z0-9\s]', password)):
                messagebox.showinfo("Strong Password", "Your password is strong")
                return
            
        else:
            messagebox.showwarning("Password Criteria", "Please enter a valid password.")

    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# TKinter window set up
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x300")

# entry widget for password input
entry = tk.Entry(root, show="*")
entry.pack(pady=20)

# button to check the password
check_button = tk.Button(root, text="Check Password", command=check_password)
check_button.pack(pady=10)

# run the application
root.mainloop()

            
      



        

       



    