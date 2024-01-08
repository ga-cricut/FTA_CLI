import BifrostController
import MachineController
import bifrost_client_api_pb2
import time

# Global Variables declaration
Motor_Connnected = True
Dev_Board = True

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

# Time compensation for homing sequence
if Motor_Connnected == True:
    print("Wait for machine to finish the homimg sequence")
    time.sleep(30)

# Disconnect with the machine and quit the proccess
und.disconnect()
# cli.quit()
 
# Lunch the bifrost proccess 
cli.launch()

# Connect to the machine
und.connect(Dev_Board)

# Generate handshake and check if it's done successfully
handshake_response = und.handshake()
if handshake_response.status != bifrost_client_api_pb2.CONNECTION_HANDSHAKE_STATUS_OK: # type: ignore
  print("Handshake failed")
  exit(1)

# Informs device if we are ready to start a plot
Plot_Ready_Response = und.plot_ready()
print(Plot_Ready_Response)

# Start Fill Engrave
# fill_engrave(number_of_passes, acceleration_x, acceleration_y, velocity_x, velocity_y, intensity, pulses_per_inch, lines_per_inch)
Plot_State_Change_Response = und.fill_engrave(1, 350, 350, 20, 12, 0, 8, 8)
print(Plot_State_Change_Response)

# Disconnect with the machine and quit the proccess
und.disconnect()
cli.quit()