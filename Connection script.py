# This script connects to a Cisco IOS device and retrieves the IP interface brief information.

from netmiko import ConnectHandler
from getpass import getpass

# Prompt for username and password
username = getpass("Enter your username: ")
password = getpass("Enter your password: ")

# Prompt for connection type
connection_type = input("Is this an SSH or COM port connection? (Enter 'ssh' or 'com'): ").strip().lower()

# Initialize connection details
connection_details = {
    "device_type": "cisco_ios",
    "username": username,
    "password": password,
}

# If SSH, prompt for IP address; if COM, prompt for COM port
if connection_type == "ssh":
    ip_address = input("Enter the IP address of the device: ").strip()
    connection_details["host"] = ip_address
elif connection_type == "com":
    com_port = input("Enter the COM port (e.g., COM3): ").strip()
    connection_details["port"] = com_port
    connection_details["device_type"] = "terminal_server"  # Adjust device_type for COM port
else:
    print("Invalid connection type. Please enter 'ssh' or 'com'.")
    exit()

# Connect to the device and retrieve output
try:
    print(f"Connecting to the device via {connection_type.upper()}...")
    connection = ConnectHandler(**connection_details)
    output = connection.send_command("show ip interface brief")
    print(f"Output from the device:\n{output}")
    connection.disconnect()
except Exception as e:
    print(f"Failed to connect to the device: {e}")
