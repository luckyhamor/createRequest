import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import subprocess

server_process = None  # Global variable to store the server process
server_running = False  # Flag to track server state

def create_json():
    # Check if output.json already exists
    try:
        with open("output.json", "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # Collect data from entries
    path_name = path_name_entry.get()
    method = method_var.get()
    content = content_entry.get()
    headers = []

    # Parse headers
    for line in headers_listbox.get(0, tk.END):
        header_name, header_value = line.split(":")
        headers.append({"header": [header_name, header_value]})

    # Append data to the list
    new_request = {
        "pathName": path_name,
        "method": method,
        "content": content,
        "headers": headers
    }

    existing_data.append(new_request)

    # Serialize data to JSON
    json_data = json.dumps(existing_data, indent=4)

    # Save JSON to a file
    with open("output.json", "w") as file:
        file.write(json_data)

    # Show messagebox
    messagebox.showinfo("Success", "Request added to output.json.")
    
    # Clear all fields
    clear_fields()

def toggle_server():
    global server_process, server_running

    if not server_running:
        port_number = port_entry.get()
        server_process = subprocess.Popen(["dyweb", "-p", port_number, "-json", "output.json"])
        messagebox.showinfo("Success", f"Server is running on port {port_number}.")
        server_running = True
        run_server_button.config(text="Stop Server")
        disable_fields()  
    else:
        if server_process:
            server_process.terminate()
            server_process = None
            messagebox.showinfo("Success", "Server has been stopped.")

        server_running = False
        run_server_button.config(text="Run Server")
        enable_fields()  

def disable_fields():
    path_name_entry.config(state="disabled")
    method_dropdown.config(state="disabled")
    content_entry.config(state="disabled")
    headers_dropdown.config(state="disabled")
    add_header_button.config(state="disabled")
    port_entry.config(state="disabled")
    create_json_button.config(state="disabled")

def enable_fields():
    path_name_entry.config(state="normal")
    method_dropdown.config(state="normal")
    content_entry.config(state="normal")
    headers_dropdown.config(state="normal")
    add_header_button.config(state="normal")
    port_entry.config(state="normal")
    create_json_button.config(state="normal")

def clear_fields():
    path_name_entry.delete(0, tk.END)
    content_entry.delete(0, tk.END)
    headers_listbox.delete(0, tk.END)
    headers_dropdown.set("")  # Clear the selection in the dropdown
    port_entry.delete(0, tk.END)


def add_header():
    selected_header = headers_var.get()
    headers_listbox.insert(tk.END, selected_header)

# Create main window
root = tk.Tk()
root.title("Create Request")

# Increase font size and entry field dimensions
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12))
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TEntry', font=('Helvetica', 12), padding=5)
style.configure('TCombobox', font=('Helvetica', 12))
style.configure('TListbox', font=('Helvetica', 12))
root.option_add("*Font", "TkDefaultFont 12")

# Frame for inputs
input_frame = ttk.Frame(root, padding="30")
input_frame.grid(row=0, column=0, sticky="ew")

# Grid configuration for uniform column width
input_frame.columnconfigure(1, weight=1)

# Path Name
path_name_label = ttk.Label(input_frame, text="Path Name:")
path_name_label.grid(row=0, column=0, sticky="w", pady=(0, 20))
path_name_entry = ttk.Entry(input_frame, width=50)
path_name_entry.grid(row=0, column=1, sticky="ew", padx=20)

# Method
method_label = ttk.Label(input_frame, text="Method:")
method_label.grid(row=1, column=0, sticky="w", pady=(0, 20))
method_var = tk.StringVar(root)
method_var.set("GET")  # Default value
method_dropdown = ttk.Combobox(input_frame, textvariable=method_var, values=["GET", "POST", "PUT", "DELETE", "PATCH"], width=47)
method_dropdown.grid(row=1, column=1, sticky="ew", padx=20)

# Content
content_label = ttk.Label(input_frame, text="Content:")
content_label.grid(row=2, column=0, sticky="w", pady=(0, 20))
content_entry = ttk.Entry(input_frame, width=50)
content_entry.grid(row=2, column=1, sticky="ew", padx=20)

# Headers
headers_label = ttk.Label(input_frame, text="Headers:")
headers_label.grid(row=3, column=0, sticky="w", pady=(0, 20))
headers_frame = ttk.Frame(input_frame)
headers_frame.grid(row=3, column=1, sticky="ew", padx=20)

headers_var = tk.StringVar(root)
headers_values = [
   "Content-type:text/plain",
   "Content-type:text/html",
   "Content-type:text/css",
   "Content-type:text/javascript",
   "Content-type:text/xml",
   "Content-type:application/json",
   "Content-type:application/xml",
   "Content-type:application/xhtml+xml",
   "Content-type:application/pdf",
   "Content-type:application/octet-stream",
   "Content-type:image/jpeg",
   "Content-type:image/png",
   "Content-type:image/gif",
   "Content-type:image/svg+xml",
   "Content-type:audio/mpeg",
   "Content-type:audio/wav",
   "Content-type:video/mp4",
   "Content-type:video/webm",
   "Content-type:multipart/form-data",
   "Content-type:multipart/byteranges",
   "Content-type:application/vnd.ms-excel",
   "Content-type:application/vnd.openxmlformats-officedocument.wordprocessingml.document",
   "Content-type:application/vnd.ms-powerpoint",
   "Content-type:application/zip",
   "Content-type:font/woff",
   "Content-type:font/woff2",
   "Content-type:application/vnd.ms-fontobject",
   "Content-type:message/rfc822",
   "Content-type:message/http",
   "Content-type:model/3mf",
   "Content-type:model/gltf+json",
   "Content-type:chemical/x-pdb"
]
headers_dropdown = ttk.Combobox(headers_frame, textvariable=headers_var, values=headers_values, width=45)
headers_dropdown.grid(row=0, column=0, sticky="ew")

add_header_button = ttk.Button(headers_frame, text="Add Header", command=add_header, width=12)
add_header_button.grid(row=0, column=1, padx=10)

headers_listbox = tk.Listbox(input_frame, height=4, width=50)
headers_listbox.grid(row=4, column=0, columnspan=2, pady=(0, 20), sticky="ew")

# Button to create / add request
create_request_button = ttk.Button(input_frame, text="Create / Add Request", command=create_json)
create_request_button.grid(row=5, column=0, columnspan=2, pady=(40, 10))

port_label = ttk.Label(input_frame, text="Port Number:")
port_label.grid(row=6, column=0, sticky="e", pady=(50, 5))
port_entry = ttk.Entry(input_frame, width=10)  # Shorter width
port_entry.grid(row=6, column=1, sticky="w", pady=(50, 5))

# Button to run server
run_server_button = ttk.Button(input_frame, text="Run Server", command=toggle_server)
run_server_button.grid(row=6, column=1, sticky="e", pady=(55, 5))

root.mainloop()
