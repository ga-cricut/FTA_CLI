import bifrost_client_api_pb2
from google.protobuf import text_format
import time

class Machine:

    def __init__(self, bifrost, device_id, bootloader_id):
        self.bifrost = bifrost
        self.device_id = device_id
        self.bootloader_id = bootloader_id

    def connect(self):
        if self.device_id == "underminer_usb_serial_0" or self.device_id == "underminer_usb_serial_1":
            self.bifrost.send("connect attach device " + self.device_id)
        elif self.device_id == "underminer":
            self.bifrost.send("connect_tcp_ip attach device_type " + self.device_id)
            self.bifrost.wait_for("on_device_connected")
        else:
            print("Connection Fail: Check the device id")

    def connect_bootloader(self):
        if self.bootloader_id == "underminer_bootloader_usb_hid_0" or self.bootloader_id == "underminer_bootloader_usb_hid_1":
            self.bifrost.send("connect attach device " + self.bootloader_id)
            self.bifrost.wait_for("on_device_connected")
        elif self.bootloader_id == "underminer_bootloader_ip_tcp_0" or self.bootloader_id == "underminer_bootloader_ip_tcp_1":
            self.disconnect()
            self.bifrost.quit()
            self.bifrost.launch()
            self.bifrost.send("connect_tcp_ip attach device_type underminer_bootloader")
            self.bifrost.wait_for("on_device_connected")
        else:
            print("Connection Fail: Check the bootloader id")

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
        if self.device_id == "underminer":
            self.bifrost.send("firmware_update device " + self.bootloader_id + " file Firmware/und_v50020.9_X10_pb18.8.bin.enc")
            return None
        else:
            self.bifrost.send("firmware_update device " + self.bootloader_id + " file Firmware/und_v50020.9_X10_pb18.8.bin.enc")
            proto_string = self.bifrost.parse_proto_string()
            firmware_update_finished_response = bifrost_client_api_pb2.FirmwareUpdateFinishedResponse()
            text_format.Parse(proto_string, firmware_update_finished_response)
            self.bifrost.wait_for("on_device_disconnected")
            return firmware_update_finished_response
    
    def plot_ready(self):
        print("parent class: plot_read")
        pass   
    
    def fill_engrave(self):
        print("parent class: fill_engrave")
        pass
    
class Underminer(Machine):

    def __init__(self, bifrost, device_id, bootloader_id):
        super().__init__(bifrost, device_id, bootloader_id)

    def plot_ready(self):
        self.bifrost.send("plot_ready ready_to_plot true")
        proto_string = self.bifrost.parse_proto_string()
        Plot_Ready_Response = bifrost_client_api_pb2.PlotReadyResponse()
        text_format.Parse(proto_string, Plot_Ready_Response)
        return Plot_Ready_Response

    def fill_engrave(self, number_of_passes, acceleration_x, acceleration_y, velocity_x, velocity_y, intensity, pulses_per_inch, lines_per_inch):
        print("Underminer Class")
        self.bifrost.send("score file 24X1_Rectangle_Path.txt\
                           svg_file false\
                           number_of_passes %d\
                           z_focus_depth 1.78\
                           material_height 0.118\
                           acceleration_x %d\
                           acceleration_y %d\
                           velocity_x %d\
                           velocity_y %d\
                           intensity %d\
                           pulses_per_inch %d\
                           lines_per_inch %d\
                           flip_pattern_direction true\
                           update_period_ms 1500\
                           intensity_interpolation_mode linear"\
                           % (number_of_passes, acceleration_x, acceleration_y, velocity_x, velocity_y, intensity, pulses_per_inch, lines_per_inch))
        proto_string = self.bifrost.parse_proto_string()
        Plot_State_Change_Response = bifrost_client_api_pb2.PlotStateChangeResponse()
        text_format.Parse(proto_string, Plot_State_Change_Response)
        return Plot_State_Change_Response
    
class Dumbledore(Machine):

    def __init__(self, bifrost, device_id, bootloader_id):
        super().__init__(bifrost, device_id, bootloader_id)