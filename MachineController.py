import bifrost_client_api_pb2
from google.protobuf import text_format
import time

class Machine:

    def __init__(self, bifrost, device_id, bootloader_id):
        self.bifrost = bifrost
        self.device_id = device_id
        self.bootloader_id = bootloader_id

    def connect(self):
        self.bifrost.send("connect attach device " + self.device_id)

    def connect_tcp_ip(self):
        self.bifrost.send("connect_tcp_ip attach device_type " + self.device_id)
        self.bifrost.wait_for("on_device_connected")

    def connect_bootloader(self):
        self.bifrost.send("connect attach device " + self.bootloader_id)
        self.bifrost.wait_for("on_device_connected")

    def handshake(self):
        self.bifrost.send("handshake")
        proto_string = self.bifrost.parse_proto_string()
        handshake_response = bifrost_client_api_pb2.ConnectionHandshakeResponse()
        text_format.Parse(proto_string, handshake_response)
        return handshake_response

    def device_information(self):
        self.bifrost.send("device_information")
        proto_string = self.bifrost.parse_proto_string()
        device_info_response = bifrost_client_api_pb2.DeviceInformationResponse()
        text_format.Parse(proto_string, device_info_response)
        return device_info_response

    def disconnect(self):
        self.bifrost.send("disconnect")
        self.bifrost.wait_for("on_device_disconnected")

    def home(self, x = True, y = True, z = True):
        command = "move_home x %r y %r z %r" % (x, y, z)
        self.bifrost.send(command.lower())
        proto_string = self.bifrost.parse_proto_string()
        move_response = bifrost_client_api_pb2.MoveResponse()
        text_format.Parse(proto_string, move_response)
        return move_response

    def move_absolute(self, x, y, z):
        self.bifrost.send("move_absolute x %f y %f z %f" % (x, y, z))
        proto_string = self.bifrost.parse_proto_string()
        move_response = bifrost_client_api_pb2.MoveResponse()
        text_format.Parse(proto_string, move_response)
        return move_response

    def product_activation_get_state(self):
      self.bifrost.send("product_activation subcommand get_state")
      proto_string = self.bifrost.parse_proto_string()
      activation_state_response = bifrost_client_api_pb2.GetProductActivatedStateResponse()
      text_format.Parse(proto_string, activation_state_response)
      return activation_state_response

    def reboot_to_bootloader(self):
        self.bifrost.send("reboot_to_bootloader")
        proto_string = self.bifrost.parse_proto_string()
        Reboot_Response = bifrost_client_api_pb2.RebootResponse()
        text_format.Parse(proto_string, Reboot_Response)
        return Reboot_Response

    def firmware_update(self):
        self.bifrost.send("firmware_update device " + self.bootloader_id + " file und_v50020.9_X10_pb18.8.bin.enc")
        proto_string = self.bifrost.parse_proto_string()
        firmware_update_finished_response = bifrost_client_api_pb2.FirmwareUpdateFinishedResponse()
        text_format.Parse(proto_string, firmware_update_finished_response)
        self.bifrost.wait_for("on_device_disconnected")
        return firmware_update_finished_response
    
class Underminer(Machine):

    def __init__(self, bifrost, device_id, bootloader_id):
        super().__init__(bifrost, device_id, bootloader_id)

class Dumbledore(Machine):

    def __init__(self, bifrost, device_id, bootloader_id):
        super().__init__(bifrost, device_id, bootloader_id)