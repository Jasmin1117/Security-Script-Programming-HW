import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from scapy.all import sniff, IP, TCP, UDP, ICMP
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Network Traffic Analyzer")
root.geometry("900x600")

# Create a label
label = tk.Label(root, text="Network Traffic Analyzer", font=("Arial", 16, "bold"))
label.pack(pady=10)

# Dropdown for selecting protocol
protocol_label = tk.Label(root, text="Select Protocol:")
protocol_label.pack()
protocol_var = tk.StringVar()
protocol_dropdown = ttk.Combobox(root, textvariable=protocol_var, values=["All", "TCP", "UDP", "ICMP"])
protocol_dropdown.current(0)  # Default to "All"
protocol_dropdown.pack()

# Entry field for filtering by port
port_label = tk.Label(root, text="Enter Port (Optional):")
port_label.pack()
port_entry = tk.Entry(root)
port_entry.pack()

# Button to start capturing packets
start_button = tk.Button(root, text="Start Capture", command=lambda: start_sniffing(), font=("Arial", 12))
start_button.pack(pady=5)

# Scrolled text area to display captured packets
text_area = scrolledtext.ScrolledText(root, width=100, height=15, font=("Courier", 10))
text_area.pack(pady=10)

# Matplotlib Figure for visualization
fig, ax = plt.subplots()
ax.set_title("Packet Traffic Over Time")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Packets")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

# Data for plotting
x_data = []
y_data = []
start_time = time.time()

# Function to update the graph
def update_plot():
    ax.clear()
    ax.set_title("Packet Traffic Over Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Packets")
    ax.plot(x_data, y_data, color="blue", marker="o", linestyle="-")
    canvas.draw()
    root.after(1000, update_plot)

# Function to process and display packets
def process_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = "Other"
        port_info = ""

        # Identify protocol
        if TCP in packet:
            proto = "TCP"
            port_info = f"Source Port: {packet[TCP].sport}, Destination Port: {packet[TCP].dport}"
        elif UDP in packet:
            proto = "UDP"
            port_info = f"Source Port: {packet[UDP].sport}, Destination Port: {packet[UDP].dport}"
        elif ICMP in packet:
            proto = "ICMP"

        # Get user-selected filters
        selected_protocol = protocol_var.get()
        selected_port = port_entry.get().strip()

        # Apply filtering logic
        if selected_protocol != "All" and selected_protocol != proto:
            return  # Skip if the protocol doesn't match
        if selected_port and port_info and selected_port not in port_info:
            return  # Skip if the port doesn't match

        # Format and display packet details
        packet_info = f"Protocol: {proto}, Source IP: {src_ip}, Destination IP: {dst_ip}, {port_info}\n"
        text_area.insert(tk.END, packet_info)
        text_area.see(tk.END)

        # Update graph
        current_time = time.time() - start_time
        x_data.append(current_time)
        y_data.append(len(x_data))

# Function to start packet sniffing in a separate thread
def start_sniffing():
    text_area.insert(tk.END, "Capturing packets...\n")
    sniff_thread = threading.Thread(target=sniff, kwargs={"prn": process_packet, "store": False}, daemon=True)
    sniff_thread.start()

# Start graph updating
update_plot()

# Start the Tkinter event loop
root.mainloop()
