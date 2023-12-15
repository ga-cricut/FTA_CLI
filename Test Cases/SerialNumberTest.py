import BifrostController
import bifrost_client_api_pb2
import MachineController

cli = BifrostController.Bifrost()
cli.print_stdout = False
cli.launch()
und = MachineController.Underminer(cli, "underminer")
und.connect_tcp_ip()
#und = cli.underminer(cli, "underminer_usb_serial_0")
#und.connect()
handshake_response = und.handshake()
if handshake_response.status != bifrost_client_api_pb2.CONNECTION_HANDSHAKE_STATUS_OK:
  print(bifrost_client_api_pb2.CONNECTION_HANDSHAKE_STATUS_OK)
  print(handshake_response.status)
  print(cli.print())
  print("\n\nHandshake failed")
  exit(1)
device_information_response = und.device_information()
print(device_information_response.serial_number)

und.disconnect()
cli.quit()
