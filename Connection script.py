# This script connects to a Cisco IOS device and retrieves the IP interface brief information.
from getpass import getpass
from netmiko import ConnectHandler
import serial.tools.list_ports

# Prompt for username and password
username = getpass("Enter your username: ")
password = getpass("Enter your password: ")
secret = getpass("Enter your secret: ")

# Prompt for connection type
connection_type = input("SSH or COM?: ").strip().lower()

# Initialize connection details
connection_details = {
    "device_type": "cisco_ios",
    "username": username,
    "password": password,
    "secret": secret,
}

# If SSH, prompt for IP address; if COM, prompt for COM port
if connection_type == "ssh":
    ip_address = input("Enter the IP address of the device: ").strip()
    connection_details["host"] = ip_address
elif connection_type == "com":

    ports = list(serial.tools.list_ports.comports())
    print("Available COM Ports:")
    for i, port in enumerate(ports, start=1):
        print(f"  {i}. {port.device} - {port.description}")
    com_port = input("Enter selection (e.g., 1, 2, 3, etc.): ").strip().upper()

    if com_port.startswith("COM"):
        port_num = com_port[3:]
        if port_num.isdigit() and int(port_num) >= 10:
            com_port = rf"\\.\{com_port}"

    connection_details["device_type"] = "cisco_ios_serial"
    connection_details["port"] = com_port
    connection_details["serial_settings"] = {
        "port": com_port,
        "baudrate": 9600,
        "bytesize": 8,
        "parity": "N",
        "stopbits": 1,
        "timeout": 1.0,
    }
    connection_details["session_log"] = "serial_debug.log"


else:
    print("Invalid connection type. Please enter 'ssh' or 'com'.")
    exit()
# Connect to the device and retrieve output
try:
    print(f"Connecting to the device via {connection_type.upper()}...")
    connection = ConnectHandler(**connection_details)
    
    # Disable short outputs
    connection.send_command("term len 0")

    # Send the first command
    output1 = connection.send_command("show ip interface brief")
    print(f"sh ip int br:\n{output1}")
    
    # Uncomment below command lines as needed
    #output2 = connection.send_command("show version")
    #print(f"second command:\n{output2}")
    
    #output3 = connection.send_command("show running-config")
    #print(f"third command:\n{output3}")

    #output4 = connection.send_command("show startup-config")
    #print(f"fourth command:\n{output4}")
    
except Exception as e:
    print(f"Failed to connect to the device: {e}")
finally:  # If the connection is still open, disconnect
    if 'connection' in locals():
        connection.disconnect()
        print("\nSession ended.")
