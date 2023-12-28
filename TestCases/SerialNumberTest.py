import BifrostController
import bifrost_client_api_pb2
import MachineController

def run(cli=None, machine=None):
  if(cli is None):
    print("Creating CLI")
    cli = BifrostController.Bifrost()
    cli.print_stdout = False
    cli.launch()
  if(machine is None):
    print("Creating Machine")
    machine = MachineController.Underminer(cli, "underminer", None)
    machine.connect_tcp_ip()
    #machine = MachineController.Underminer(cli, "underminer_usb_serial_0")
    #machine.connect()
    handshake_response = machine.handshake()
    if handshake_response.status != bifrost_client_api_pb2.CONNECTION_HANDSHAKE_STATUS_OK:
      print(bifrost_client_api_pb2.CONNECTION_HANDSHAKE_STATUS_OK)
      print(handshake_response.status)
      print(cli.print())
      print("\n\nHandshake failed")
      exit(1)

  device_information_response = machine.device_information()
  print(device_information_response.serial_number)

  machine.disconnect()
  cli.quit()
