from netmiko import ConnectHandler
import serial.tools.list_ports
from getpass import getpass

# List available COM ports and prompt user to select
ports = list(serial.tools.list_ports.comports())
print("Available COM Ports:")
for i, port in enumerate(ports, start=1):
    print(f"  {i}. {port.device} - {port.description}")

selection = input("Enter the number of the COM port to use: ").strip()

try:
    index = int(selection) - 1
    com_port = ports[index].device
except (ValueError, IndexError):
    print("Invalid selection.")
    exit(1)

# Prompt user for credentials
username = input("Username: ").strip()
password = getpass("Password: ")
secret = getpass("Enable secret (leave blank if none): ")

print(f"\nConnecting to {com_port}...")

# Definine connection to the selected serial device
device = {
    "device_type": "cisco_ios_serial",
    "username": username,
    "password": password,
    "secret": secret if secret else None,
    "serial_settings": {
        "port": com_port,
        "baudrate": 9600,
        "bytesize": 8,
        "parity": "N",
        "stopbits": 1,
        "timeout": 1,
    },
}

# Connect to device
connection = ConnectHandler(**device)

# Enter Enable mode (if applicable)
if secret:
    connection.enable()

# Commands to send - uncomment as needed.
commands = [
    "show ip int br",
    # "sh ver",
    # "sh run",
    # "sh int status",
]

# Run the commands and output
for i in commands:
    print(f"\n{i}\n")
    output = connection.send_command(i)
    print(output)

# Disconnect
connection.disconnect()
