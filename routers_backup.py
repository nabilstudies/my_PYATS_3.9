import csv
from netmiko import ConnectHandler
import datetime

def connect_to_device(device):
    return ConnectHandler(**device)

def get_device_config(net_connect, device_name):
    config = net_connect.send_command("show running-config")
    return config

def save_config(device_name, config):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{device_name}_{timestamp}.cfg"
    with open(filename, "w") as file:
        file.write(config)
    print(f"Configuration saved as {filename}")

# Path to the CSV file
csv_file = "routers_csv.txt"

# Read the device details from the CSV file
devices = []
try:
    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            devices.append(row)
except FileNotFoundError:
    print(f"CSV file '{csv_file}' not found.")
    exit(1)
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")
    exit(1)

# Print the device details
print("Device Details:")
for device in devices:
    print(device)

# Connect to each device, get the configuration, and save it
for device in devices:
    try:
        device_name = device[0]  # Assuming IP is in the first column
        device_info = {
            "device_type": device[1],  # Assuming device type is in the second column
            "ip": device[0],  # Assuming IP is in the first column
            "username": device[2],  # Assuming username is in the third column
            "password": device[3],  # Assuming password is in the fourth column
        }
        net_connect = connect_to_device(device_info)
        config = get_device_config(net_connect, device_name)
        save_config(device_name, config)
        net_connect.disconnect()
    except Exception as e:
        print(f"Error occurred for device '{device_name}': {e}")
