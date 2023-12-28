import typer
from typing_extensions import Annotated
from TestCases import SerialNumberTest
import MachineController
import BifrostController
import bifrost_client_api_pb2

initialized = False
CLI = None
MACHINE = None

app = typer.Typer()

def initialize():
    global initialized
    global CLI
    global MACHINE
    print("Initialize")
    CLI = BifrostController.Bifrost()
    CLI.print_stdout = False
    CLI.launch()
    MACHINE = MachineController.Underminer(CLI, "underminer", None)
    MACHINE.connect_tcp_ip()
    handshake_response = MACHINE.handshake()
    if handshake_response.status != bifrost_client_api_pb2.CONNECTION_HANDSHAKE_STATUS_OK:
        print(bifrost_client_api_pb2.CONNECTION_HANDSHAKE_STATUS_OK)
        print(handshake_response.status)
        print(CLI.print())
        print("\n\nHandshake failed")
        exit(1)

    initialized = True

def run_serial_number_test():
    global initialized
    print("Serial Number Test")
    if initialized:
        SerialNumberTest.run(CLI, MACHINE)
    else:
        SerialNumberTest.run()

    initialized = False

app.command()(initialize)
app.command()(run_serial_number_test)

if __name__ == "__main__":
    app()
