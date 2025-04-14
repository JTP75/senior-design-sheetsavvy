import traceback
import warnings

import serial
import serial.tools.list_ports
import json

from src.framework.serial_interface import SerialInterface
from src.framework.serial_interface_exception import SerialInterfaceException


def get_available_ports() -> list:
    return list(serial.tools.list_ports.comports())

class SerialInterfaceImpl(SerialInterface):

    port: str
    baudrate: int
    _serial: serial.Serial

    json_data: dict

    ux: any
    prepare_sheet_music: any

    device_state: str

    def __init__(self, port: str, baudrate: int):
        self.port = port
        self.baudrate = baudrate
        # noinspection PyTypeChecker
        self._serial = None
        self.ux = None
        self.prepare_sheet_music = None
        self.json_data = {}
        self.device_state = "disconnected"

    def check_com_list(self) -> bool:
        for port in get_available_ports():
            if port.name==self.port:
                return True
        return False

    def open(self):
        if not self.is_open():
            self._serial = serial.Serial(self.port, self.baudrate, timeout=1)

    def close(self):
        if self.is_open():
            self._serial.close()

    def is_open(self):
        return self._serial.is_open if self._serial else False

    async def read_in_serial(self):
        if not self.ux: return

        try:
            self.open()
            while not self.device_state=="sending":
                self._update_state()
            self._read_data()
            while not self.device_state=="idle":
                self._update_state()
            self.close()
        except serial.SerialException as serial_error:
            traceback.print_exc()

        self.prepare_sheet_music()
        self.ux.send_ready_to_save(True)

    def _await_message(self, target):
        while True:
            line = self._readline()
            if line==target: break

    def _update_state(self):
        if not self.is_open():
            self.device_state = "disconnected"
        line = self._readline()
        if line == "STATE: IDLE":
            self.device_state = "idle"
        elif line == "STATE: COUNTOFF":
            self.device_state = "countoff"
        elif line == "STATE: RECORDING":
            self.device_state = "recording"
        elif line == "STATE: SENDING":
            self.device_state = "sending"
        self.ux.send_device_state(self.device_state)

    def _read_data(self):
        if not self.is_open():
            raise SerialInterfaceException("Serial port is not open")
        assert(self.device_state=="sending")
        received_note_data = False
        received_attr_data = False
        while not (received_attr_data and received_note_data):
            line = self._readline()
            if line=="BEGIN ATTRIBUTES":
                self._read_attr_data()
                received_attr_data = True
            elif line=="BEGIN NOTES":
                self._read_note_data()
                received_note_data = True

    def _read_note_data(self):
        data = []
        while True:
            line = self._readline()
            if line=="END NOTES": break
            if line!="": data.append(json.loads(line))
        self.json_data["notes"] = data

    def _read_attr_data(self):
        line = self._readline()
        self.json_data["attributes"] = json.loads(line)
        while True:
            line = self._readline()
            if line=="END ATTRIBUTES": break

    def _readline(self) -> str:

        try:
            line = self._serial.readline().decode("utf-8").strip()

        except UnicodeDecodeError as error:
            warnings.warn(error.reason)
            return ""

        return line if line else ""
