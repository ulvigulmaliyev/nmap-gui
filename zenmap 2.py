import os
import re
import tkinter as tk
from tkinter import scrolledtext, ttk

# Predefined Nmap script categories
nmap_script_categories = ['default', 'vuln', 'auth', 'broadcast', 'discovery', 'safe', 'intrusive']

# Default profiles for Nmap scans
default_profiles = {
    "Quick Scan": {
        "scan_type": "-sS",
        "verbose": False,
        "os_detection": False,
        "service_version": False,
        "ping_scan": False,
        "dns_disable": False,
        "ports": "1-100",
        "timing": "3",
        "top_ports": "",
        "script": ""
    },
    "Intense Scan": {
        "scan_type": "-sS",
        "verbose": True,
        "os_detection": True,
        "service_version": True,
        "ping_scan": False,
        "dns_disable": False,
        "ports": "",
        "timing": "4",
        "top_ports": "",
        "script": ""
    },
    "Ping Scan": {
        "scan_type": "-sn",
        "verbose": False,
        "os_detection": False,
        "service_version": False,
        "ping_scan": True,
        "dns_disable": False,
        "ports": "",
        "timing": "",
        "top_ports": "",
        "script": ""
    },
}

# Function to update the command preview
def update_command_preview(*args):
    target = target_entry.get()  # Get target from entry
    scan_type = scan_type_var.get()  # Get scan type
    verbose = verbose_var.get()  # Get verbose option
    os_detection = os_var.get()  # Get OS detection option
    service_version = version_var.get()  # Get service version detection option
    ping_scan = ping_var.get()  # Get ping scan option
    dns_disable = dns_var.get()  # Get DNS resolution disable option
    ports = ports_entry.get()  # Get ports from entry
    timing = timing_var.get()  # Get timing template
    top_ports = top_ports_entry.get()  # Get top ports number
    script = script_var.get()  # Get script choice

    # Build the Nmap command preview dynamically
    nmap_command = f"nmap {scan_type}"

    if verbose:
        nmap_command += " -v"
    if os_detection:
        nmap_command += " -O"
    if service_version:
        nmap_command += " -sV"
    if ping_scan:
        nmap_command += " -sn"
    if dns_disable:
        nmap_command += " -n"
    if ports:
        nmap_command += f" -p {ports}"
    if timing:
        nmap_command += f" -T{timing}"
    if top_ports:
        nmap_command += f" --top-ports {top_ports}"

    if script:
        nmap_command += f" --script={script}"

    if target:
        nmap_command += f" {target}"

    # Update the preview box with the built command
    command_preview_box.delete(1.0, tk.END)
    command_preview_box.insert(tk.END, nmap_command)

# Function to load selected profile
def load_profile(event):
    profile_name = profile_var.get()
    profile = default_profiles[profile_name]

    # Update scan options based on the selected profile
    scan_type_var.set(profile["scan_type"])
    verbose_var.set(profile["verbose"])
    os_var.set(profile["os_detection"])
    version_var.set(profile["service_version"])
    ping_var.set(profile["ping_scan"])
    dns_var.set(profile["dns_disable"])
    ports_entry.delete(0, tk.END)
    ports_entry.insert(0, profile["ports"])
    timing_var.set(profile["timing"])
    top_ports_entry.delete(0, tk.END)
    top_ports_entry.insert(0, profile["top_ports"])
    script_var.set(profile["script"])

    # Update command preview for the selected profile
    update_command_preview()

# Function to run Nmap and display results
def run_nmap():
    target = target_entry.get()
    if not target:
        output_text.insert(tk.END, "Please enter a target to scan.\n")
        return

    # Update command preview
    update_command_preview()

    # Get the command from the preview box (what the user sees)
    nmap_command = command_preview_box.get(1.0, tk.END).strip() + " > nmap_output.txt"

    # Execute the Nmap command
    os.system(nmap_command)

    # Read and display the output from the file
    with open('nmap_output.txt', 'r') as file:
        output = file.read()

    # Clear previous results
    output_text.delete(1.0, tk.END)

    # Display the full result in the main output text area
    output_text.insert(tk.END, output)

    # Parse open ports and services to show in side panel
    parse_and_display_ports(output)

    # Optionally remove the temporary file after reading
    os.remove('nmap_output.txt')

# Function to parse Nmap output and extract open ports and services
def parse_and_display_ports(nmap_output):
    open_ports_panel.delete(0, tk.END)  # Clear previous results

    # Use regex to find open ports and services (simplified example)
    open_ports = re.findall(r"(\d+)/tcp\s+open\s+(\S+)", nmap_output)

    if open_ports:
        for port, service in open_ports:
            open_ports_panel.insert(tk.END, f"Port: {port}, Service: {service}")
    else:
        open_ports_panel.insert(tk.END, "No open ports found.")

# Create the main window
root = tk.Tk()
root.title("Nmap GUI")

# Create frames for organizing layout
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Top frame: Command options
target_label = tk.Label(top_frame, text="Target (IP/Hostname):")
target_label.grid(row=0, column=0, padx=5, pady=5)

target_entry = tk.Entry(top_frame, width=30)
target_entry.grid(row=0, column=1, padx=5, pady=5)

scan_type_var = tk.StringVar(root)
scan_type_var.set("-sS")  # Default value for SYN scan

scan_type_label = tk.Label(top_frame, text="Scan Type:")
scan_type_label.grid(row=0, column=2, padx=5, pady=5)

scan_type_menu = tk.OptionMenu(top_frame, scan_type_var, "-sS", "-sP", "-sV", "-O", "-sn")
scan_type_menu.grid(row=0, column=3, padx=5, pady=5)

ports_label = tk.Label(top_frame, text="Ports (-p):")
ports_label.grid(row=1, column=0, padx=5, pady=5)

ports_entry = tk.Entry(top_frame, width=10)
ports_entry.grid(row=1, column=1, padx=5, pady=5)

timing_label = tk.Label(top_frame, text="Timing Template (-T):")
timing_label.grid(row=1, column=2, padx=5, pady=5)

timing_var = tk.StringVar(root)
timing_var.set("3")  # Default to normal timing
timing_menu = tk.OptionMenu(top_frame, timing_var, "0", "1", "2", "3", "4", "5")
timing_menu.grid(row=1, column=3, padx=5, pady=5)

top_ports_label = tk.Label(top_frame, text="Top Ports (--top-ports):")
top_ports_label.grid(row=2, column=0, padx=5, pady=5)

top_ports_entry = tk.Entry(top_frame, width=10)
top_ports_entry.grid(row=2, column=1, padx=5, pady=5)

# Checkboxes for additional options
verbose_var = tk.BooleanVar()
verbose_check = tk.Checkbutton(top_frame, text="Verbose (-v)", variable=verbose_var)
verbose_check.grid(row=3, column=0, padx=5, pady=5)

os_var = tk.BooleanVar()
os_check = tk.Checkbutton(top_frame, text="OS Detection (-O)", variable=os_var)
os_check.grid(row=3, column=1, padx=5, pady=5)

version_var = tk.BooleanVar()
version_check = tk.Checkbutton(top_frame, text="Service Version (-sV)", variable=version_var)
version_check.grid(row=3, column=2, padx=5, pady=5)

ping_var = tk.BooleanVar()
ping_check = tk.Checkbutton(top_frame, text="Ping Scan (-sn)", variable=ping_var)
ping_check.grid(row=3, column=3, padx=5, pady=5)

dns_var = tk.BooleanVar()
dns_check = tk.Checkbutton(top_frame, text="Disable DNS Resolution (-n)", variable=dns_var)
dns_check.grid(row=4, column=0, padx=5, pady=5)

# Create profiles dropdown
profile_var = tk.StringVar(root)
profile_var.set("Quick Scan")
profile_menu = ttk.Combobox(top_frame, textvariable=profile_var, values=list(default_profiles.keys()), state='readonly')
profile_menu.grid(row=4, column=1, padx=5, pady=5)
profile_menu.bind("<<ComboboxSelected>>", load_profile)

# Variable for Nmap script selection
script_var = tk.StringVar(root)
script_var.set("")  # Default to no script

script_label = tk.Label(top_frame, text="Nmap Script:")
script_label.grid(row=2, column=2, padx=5, pady=5)

script_menu = ttk.Combobox(top_frame, textvariable=script_var, values=nmap_script_categories, state='readonly')
script_menu.grid(row=2, column=3, padx=5, pady=5)

# Command preview box
command_preview_box = scrolledtext.ScrolledText(top_frame, height=1, width=100)
command_preview_box.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

# Run button
run_button = tk.Button(top_frame, text="Run Nmap", command=run_nmap)
run_button.grid(row=6, column=0, columnspan=4, padx=5, pady=5)

# Output display
output_label = tk.Label(right_frame, text="Nmap Output:")
output_label.pack()

output_text = scrolledtext.ScrolledText(right_frame, height=20, width=80)
output_text.pack(padx=5, pady=5)

# Open ports panel
open_ports_label = tk.Label(left_frame, text="Open Ports:")
open_ports_label.pack()

open_ports_panel = tk.Listbox(left_frame, width=40)
open_ports_panel.pack(padx=5, pady=5)

# Initial command preview
update_command_preview()

# Run the GUI
root.mainloop()
