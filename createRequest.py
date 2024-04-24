import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import subprocess

def toggle_button():
    if is_server_running():
        stop_command()
    else:
        create_json()

def is_server_running():
    port_number = port_entry.get()
    result = subprocess.run(["lsof", "-ti", f":{port_number}"], capture_output=True, text=True)
    return bool(result.stdout.strip())

def add_header():
    selected_header = headers_var.get()
    headers_listbox.insert(tk.END, selected_header)

def create_json():
    data = []

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
    data.append({
        "pathName": path_name,
        "method": method,
        "content": content,
        "headers": headers
    })

    # Serialize data to JSON
    json_data = json.dumps(data, indent=4)

    # Save JSON to a file
    with open("output.json", "w") as file:
        file.write(json_data)

    # Get the port number
    port_number = port_entry.get()

    # Show messagebox
    messagebox.showinfo("Success", f"JSON file was created and running on port {port_number}")

    # Execute dyweb command
    subprocess.Popen(["dyweb", "-p", port_number, "-json", "output.json"])

    toggle_button.config(text="Stop Server", command=stop_command)
    # Disable fields
    path_name_entry.config(state="disabled")
    method_dropdown.config(state="disabled")
    content_entry.config(state="disabled")
    headers_dropdown.config(state="disabled")
    add_header_button.config(state="disabled")
    port_entry.config(state="disabled")

def stop_command():
    port_number = port_entry.get()
    lsof_process = subprocess.Popen(["lsof", "-ti", f":{port_number}"], stdout=subprocess.PIPE)
    xargs_process = subprocess.Popen(["xargs", "kill"], stdin=lsof_process.stdout, stdout=subprocess.PIPE)
    lsof_process.stdout.close()  # Close lsof's stdout to prevent deadlocks
    lsof_process.wait()  # Wait for lsof to finish
    xargs_process.communicate()  # Wait for xargs to finish

    messagebox.showinfo("Success", f"Command running on port {port_number} has been stopped.")

    # Enable fields first
    enable_fields()
    # Clear fields after enabling them
    clear_fields()

    toggle_button.config(text="Create and Run server", command=create_json)

def clear_fields():
    path_name_entry.delete(0, tk.END)
    content_entry.delete(0, tk.END)
    headers_listbox.delete(0, tk.END)
    port_entry.delete(0, tk.END)
    headers_var.set("")  # Reset dropdown value

def enable_fields():
    path_name_entry.config(state="normal")
    method_dropdown.config(state="readonly")
    content_entry.config(state="normal")
    headers_dropdown.config(state="readonly")
    add_header_button.config(state="normal")
    port_entry.config(state="normal")

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
path_name_label.grid(row=0, column=0, sticky="w", pady=(0, 40))
path_name_entry = ttk.Entry(input_frame, width=50)
path_name_entry.grid(row=0, column=1, sticky="ew", padx=40)

# Method
method_label = ttk.Label(input_frame, text="Method:")
method_label.grid(row=1, column=0, sticky="w", pady=(0, 40))
method_var = tk.StringVar(root)
method_var.set("GET")  # Default value
method_dropdown = ttk.Combobox(input_frame, textvariable=method_var, values=["GET", "POST", "PUT", "DELETE", "PATCH"], width=47)
method_dropdown.grid(row=1, column=1, sticky="ew", padx=40)

# Content
content_label = ttk.Label(input_frame, text="Content:")
content_label.grid(row=2, column=0, sticky="w", pady=(0, 40))
content_entry = ttk.Entry(input_frame, width=50)
content_entry.grid(row=2, column=1, sticky="ew", padx=40)

# Headers
headers_label = ttk.Label(input_frame, text="Headers:")
headers_label.grid(row=3, column=0, sticky="nw", pady=(0, 40))
headers_frame = ttk.Frame(input_frame)
headers_frame.grid(row=3, column=1, sticky="ew", padx=40)

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
headers_listbox.grid(row=4, column=0, columnspan=2, pady=(0, 40), sticky="ew")

# Port Number
port_label = ttk.Label(input_frame, text="Port Number:")
port_label.grid(row=5, column=0, sticky="w", pady=(0, 40))
port_entry = ttk.Entry(input_frame, width=20)
port_entry.grid(row=5, column=1, sticky="ew", padx=40)

# Button to create JSON and run or stop command
toggle_button = ttk.Button(input_frame, text="Create and Run Server", command=toggle_button)
toggle_button.grid(row=6, column=0, columnspan=2, pady=50)

root.mainloop()

