import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import subprocess

def add_header():
    selected_header = headers_var.get()
    headers_listbox.insert(tk.END, selected_header)

def save_json():
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

    # Close the Tkinter UI
    root.destroy()

    # Execute dyweb command
    subprocess.run(["dyweb", "-p", port_number, "-json", "output.json"])

# Create main window
root = tk.Tk()
root.title("Create Request")

# Frame for inputs
input_frame = ttk.Frame(root, padding="20")
input_frame.grid(row=0, column=0)

# Path Name
path_name_label = ttk.Label(input_frame, text="Path Name:")
path_name_label.grid(row=0, column=0, sticky="w")
path_name_entry = ttk.Entry(input_frame)
path_name_entry.grid(row=0, column=1)

# Method
method_label = ttk.Label(input_frame, text="Method:")
method_label.grid(row=1, column=0, sticky="w")
method_var = tk.StringVar(root)
method_var.set("GET")  # Default value
method_dropdown = ttk.Combobox(input_frame, textvariable=method_var, values=["GET", "POST", "PUT", "DELETE", "PATCH"])
method_dropdown.grid(row=1, column=1)

# Content
content_label = ttk.Label(input_frame, text="Content:")
content_label.grid(row=2, column=0, sticky="w")
content_entry = ttk.Entry(input_frame)
content_entry.grid(row=2, column=1)

# Headers
headers_label = ttk.Label(input_frame, text="Headers:")
headers_label.grid(row=3, column=0, sticky="w")

headers_frame = ttk.Frame(input_frame)
headers_frame.grid(row=3, column=1, sticky="w")

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

headers_dropdown = ttk.Combobox(headers_frame, textvariable=headers_var, values=headers_values)
headers_dropdown.grid(row=0, column=0)

add_header_button = ttk.Button(headers_frame, text="Add Header", command=add_header)
add_header_button.grid(row=0, column=1)

headers_listbox = tk.Listbox(input_frame, height=4, width=40)
headers_listbox.grid(row=4, columnspan=2, pady=5, sticky="w")

# Port Number
port_label = ttk.Label(input_frame, text="Port Number:")
port_label.grid(row=5, column=0, sticky="w")
port_entry = ttk.Entry(input_frame)
port_entry.grid(row=5, column=1)

# Button to save JSON
save_button = ttk.Button(input_frame, text="Save JSON and Run", command=save_json)
save_button.grid(row=6, columnspan=2, pady=10)

root.mainloop()

