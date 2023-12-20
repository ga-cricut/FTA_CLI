import BifrostController
import MachineController
import bifrost_client_api_pb2
import time

cli = BifrostController.Bifrost()
cli.print_stdout = False
cli.launch()
und = MachineController.Underminer(cli,"underminer_usb_serial_0", "underminer_bootloader_usb_hid_1")
und.connect()
handshake_response = und.handshake()
if handshake_response.status != bifrost_client_api_pb2.CONNECTION_HANDSHAKE_STATUS_OK: # type: ignore
  print("Handshake failed")
  exit(1)

# Put machine into bootloader
Reboot_Response = und.reboot_to_bootloader()

# Check if reboot succeed
time.sleep(1)
print(Reboot_Response)
# while Reboot_Response.reboot_successful != 1 :
#   pass

#Chill for a bit
time.sleep(5)

# Connect to the bootloader
und.connect_bootloader()

# Start Firmware update
firmware_update_finished_response = und.firmware_update()
print(firmware_update_finished_response.success)
print(firmware_update_finished_response.failure)

und.disconnect()
cli.quit()
