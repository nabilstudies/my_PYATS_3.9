import csv
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetMikoTimeoutException
import datetime
from paramiko.ssh_exception import SSHException
import os

def connect_to_device(device):
    return ConnectHandler(**device)

def get_device_config(net_connect, device_name, command):
    try:
        if command == "show running-config":
            config = net_connect.send_command(command)
            print(f'this is the output of the command: {config}')
            return config
        else:
            print("The command should be show running-config")
    except Exception as e:
        print("did not get the device config "+e)
    
def save_config(device_name, config, backup_status):
    print("this is saveconfig function")
    print(config)
    if config and os.stat("filename").st_size != 0:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{device_name}_{timestamp}.cfg"
        try:
            with open(filename, "w") as file:
                file.write(config)
            print(f"Configuration saved as {filename}")
            backup_status[device_name] = "Success"  # Update backup status
            print(backup_status[device_name])
            return True
        except Exception as e:
            if os.stat("filename").st_size == 0 :
                print(f"Error saving configuration for device '{device_name}'")
                backup_status[device_name] = "Failure"  # Update backup status
                print(backup_status[device_name])
            # print(f"Error saving configuration for device '{device_name}': {e}")
                print(f"Error saving configuration for device '{device_name}'")
                backup_status[device_name] = "Failure"  # Update backup status
                print(backup_status[device_name])
            return False
    elif config and os.stat("filename").st_size == 0:
        
        print(f"Error saving configuration for device '{device_name}'")
        backup_status[device_name] = "Failure"  # Update backup status
        print(backup_status[device_name])
        return False
   

# Path to the CSV file
csv_file = "routers_csv.txt"
backup_status = {}  # Dictionary to track backup status

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
        print(f'{device_name} this is just for testing' )
        print(f'{device_info} this is just for testing')
        net_connect = connect_to_device(device_info)
        print(net_connect+"jslkfjlksdjflskdjf")
        config = get_device_config(net_connect, device_name,'show running-config')
        print(backup_status)
        save_status = save_config(device_name, config, backup_status)  # Pass backup_status dictionary
       
        print(save_status)
        if not save_status:  # Check if save_status is False
            backup_status[device_name] = "Failed"  # Set status as "Failed"
        
        net_connect.disconnect()
  #  except Exception as e:
  #      print(f"Error occurred for device '{device_name}': {e}")
  #      continue
    except (NetMikoTimeoutException):
        print("Timeout to device : " + str(device[0]))
        #save_status = save_config(device_name, "show running-config", backup_status)  # Pass backup_status dictionary
        #print(save_status)
        continue
    except (NetmikoAuthenticationException):
        print("Authentication failure: " + str(device[0]))
        continue
    except (SSHException):
        print("Something with SSH, are you sure SSH is enabled on remote device: " + str(device[0]))
        continue
    except Exception as other_error:
        print("Some other error: " + str(other_error))
        continue

# Print backup status
print("\nBackup Status:")

for device_name, status in backup_status.items():
    print(f"Device '{device_name}': {status}")