import BifrostController
import MachineController
import bifrost_client_api_pb2
import time

# Global Variables declaration
Motor_Connnected = False
Dev_Board = False

# Creat an object of Bifrost Class
cli = BifrostController.Bifrost()

# Disable subprocess output printouts 
cli.print_stdout = True

# Lunch the bifrost proccess 
cli.launch()

# Creat an object of Underminer Class
und = MachineController.Underminer(cli)

# Connect to the machine/Loki(SW Simulator)
Device_ID = und.connect(Dev_Board)

# Generate handshake and check if it's done successfully
handshake_response = und.handshake()
if handshake_response.status != bifrost_client_api_pb2.CONNECTION_HANDSHAKE_STATUS_OK: # type: ignore
  print("Handshake failed")
  exit(1)

# Put machine into bootloader
Reboot_Response = und.reboot_to_bootloader()

# Check if reboot succeed
time.sleep(1)
print(Reboot_Response)

# # Potential optimization
# while Reboot_Response.reboot_successful != 1 :
#   pass

# Wait for bootloader to sattle
if Dev_Board:
  time.sleep(5)

# Connect to the bootloader
Bootloader_ID = und.connect_bootloader(Dev_Board)

# Start Firmware update
firmware_update_finished_response = und.firmware_update(Dev_Board,Bootloader_ID)

# Check the Firmware update status (Not printing useful information currently)
# print(firmware_update_finished_response.success)
# print(firmware_update_finished_response.failure)

# Disconnect with the machine and quit the proccess
und.disconnect()
cli.quit()
