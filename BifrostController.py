import subprocess
import time
import threading
import re
import MachineController
import os

class Bifrost:

  print_stdout = True

  def __init__(self):
    bifrost_cli_path = os.path.join(os.path.dirname(__file__), ("bifrost_swift_cli_windows_0.0.14-alpha/bifrost_cli.exe"))
    self.process_path = bifrost_cli_path

  def launch(self):
    self.cli_process = subprocess.Popen([self.process_path, '--stdio'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

  def wait_for(self, success_string):
    while(True):
      line = self.cli_process.stdout.readline()
      if self.print_stdout:
        print(line, end="")
      if (success_string in line):
        return
      if ("error: " in line):
        return

  def parse_proto_string(self):
    end_found = False
    parsing_proto_string = False
    start_index = None
    count = 0
    proto_lines = []
    while not end_found:
      line = self.cli_process.stdout.readline()
      if self.print_stdout:
        print(line, end="")
      message = self.parse_cli_line(line)
      index = 0;
      for char in message:
        if (char == "{"):
          count += 1
          if not parsing_proto_string:
            start_index = index
          parsing_proto_string = True
        if (char == "}"):
          count -= 1
          if (count == 0):
            end_found = True
            parsing_proto_string = False
        index += 1
      if start_index:
        message = message[start_index:]
        start_index = None
      if parsing_proto_string:
        proto_lines.append(message)
    proto_string = "".join(proto_lines)
    proto_string = proto_string.strip("{}")
    #print("Proto string: " + proto_string)
    return proto_string

  def parse_cli_line(self, line):
    parts = line.split()
    if len(parts) < 1:
      return line
    result = re.search("\d{1,2}:\d{2}:\d{2}\.\d{3}", parts[0])
    if result:
      message = parts[2:len(parts)]
      return " ".join(message)
    return line

  def underminer_simulator(self):
    return self.underminer("underminer")

  def underminer(self, device_id):
    return MachineController.Machine(self, device_id)

  def dumbledore(self, device_id):
    return MachineController.Machine(self, device_id)

  def quit(self):
    self.send("quit")
    for line in self.cli_process.stdout:
      if self.print_stdout:
        print(line, end="")
    self.cli_process.wait()

  def print(self):
    return self.cli_process.communicate()

  def send(self, text):
    self.cli_process.stdin.write(text + "\n")
    self.cli_process.stdin.flush()
