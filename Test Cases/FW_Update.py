import BifrostController
import bifrost_client_api_pb2
import MachineController
import time


cli = BifrostController.Bifrost()
cli.print_stdout = False
cli.launch()
# und = cli.underminer_simulator()
# und.connect_tcp_ip()
und = MachineController.Underminer(cli, "underminer_usb_serial_0", "underminer_bootloader_usb_hid_1")
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
print(firmware_update_finished_response)
device_information_response = und.device_information()
print(device_information_response.status)

und.disconnect()
cli.quit()
