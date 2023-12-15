import time
import bifrost_client_api_pb2
from google.protobuf import text_format

class Machine:

    def __init__(self, bifrost, device_id):
        self.bifrost = bifrost
        self.device_id = device_id

    def connect(self):
        self.bifrost.send("connect attach device " + self.device_id)

    def connect_tcp_ip(self):
        self.bifrost.send("connect_tcp_ip attach device_type " + self.device_id)
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