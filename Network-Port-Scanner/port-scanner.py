import tkinter as tk
from tkinter import messagebox
import socket
import threading
import re


def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        s.close()

        if result == 0:
            return f"Port {port}: Open\n"
        else:
            return f"Port {port}: Closed\n"
    except socket.error as e:
        return f"Error connecting to port {port}: {e}\n"
    

def start_scan_thread():
    ip = entry_ip.get()
    portrange = entry_port.get()

    if not ip or not portrange:
        messagebox.showerror("Invalid Input", "Please enter IP and port range.")
        return
    
    ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if not re.match(ip_pattern, ip):
        try:
            ip = socket.gethostbyname(ip)
        except socket.gaierror:
            messagebox.showerror("Error", "Invalid IP address or hostname.")
            return
        

    ports_to_scan = []

    if  "-" in portrange:
       try:
            start, end = map(int, portrange.split("-"))
            ports_to_scan = list(range(start, end + 1))
       except ValueError:
            messagebox.showerror("Error", "Invalid port range format (e.g., 20-1024).")
            return

   
    elif "," in portrange:
        try:
            ports_to_scan = [int(p) for p in portrange.split(",")]
        except ValueError:
            messagebox.showerror("Error", "Invalid port list format.")
            return

    else:
        try:
            ports_to_scan.append(int(portrange))
        except ValueError:
            messagebox.showerror("Error", "Invalid port number.")
            return
    
        
    result_text.delete("1.0", tk.END)

    def scan_and_update():
        for port in ports_to_scan:
            result = scan_port(ip, port)
            result_text.insert(tk.END, result)
            result_text.see(tk.END)

    thread = threading.Thread(target=scan_and_update)
    thread.start()


def clear_results():
    result_text.delete("1.0", tk.END)


root = tk.Tk()
root.title("Port Scanner")

label_ip = tk.Label(root, text="IP Address/Hostname:")
label_ip.grid(row=0, column=0, padx=10, pady=10)
entry_ip = tk.Entry(root, width=30)
entry_ip.grid(row=0, column=1, padx=10, pady=10)

label_port = tk.Label(root, text="Port(s) (80, 20-1024):")
label_port.grid(row=1, column=0, padx=10, pady=10)
entry_port = tk.Entry(root, width=30)
entry_port.grid(row=1, column=1, padx=10, pady=10)

scan_button = tk.Button(root, text="Scan Ports", command=start_scan_thread)
scan_button.grid(row=2, column=0, columnspan=2, pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_results)
clear_button.grid(row=3, column=0, columnspan=2, pady=10)

result_text = tk.Text(root, font=("Helvetica", 14), wrap=tk.WORD)
scrollbar = tk.Scrollbar(root)
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)
scrollbar.grid(row=4, column=2, sticky='ns')
result_text.grid(row=4, column=0, columnspan=2, pady=10, sticky='nsew')

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(4, weight=1)

root.mainloop()