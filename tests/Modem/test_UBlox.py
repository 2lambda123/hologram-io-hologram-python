# Author: Hologram <support@hologram.io>
#
# Copyright 2017 - Hologram (Konekt, Inc.)
#
# LICENSE: Distributed under the terms of the MIT License
#
# test_Ublox.py - This file implements unit tests for the Ublox modem interface.

import pytest
import sys

from Hologram.Network.Modem.UBlox import Ublox
from UtilClasses import ModemResult

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

def mock_write(Ublox, message):
    return True

def mock_read(Ublox):
    return True

def mock_readline(Ublox, timeout=None, hide=False):
    return ''

def mock_open_serial_port(Ublox, device_name=None):
    return True

def mock_close_serial_port(Ublox):
    return True

def mock_detect_usable_serial_port(Ublox, stop_on_first=True):
    return '/dev/ttyUSB0'

def mock_result(modem):
    return (ModemResult.OK, None)

@pytest.fixture
def no_serial_port(monkeypatch):
    monkeypatch.setattr(Ublox, '_read_from_serial_port', mock_read)
    monkeypatch.setattr(Ublox, '_readline_from_serial_port', mock_readline)
    monkeypatch.setattr(Ublox, '_write_to_serial_port_and_flush', mock_write)
    monkeypatch.setattr(Ublox, 'openSerialPort', mock_open_serial_port)
    monkeypatch.setattr(Ublox, 'closeSerialPort', mock_close_serial_port)
    monkeypatch.setattr(Ublox, 'detect_usable_serial_port', mock_detect_usable_serial_port)

@pytest.fixture
def override_command_result(monkeypatch):
    monkeypatch.setattr(Ublox, '_command_result', mock_result)

def test_init_Ublox_no_args(no_serial_port):
    modem = Ublox()
    assert(modem.timeout == 1)
    assert(modem.socket_identifier == 0)
    assert(modem.chatscript_file.endswith('/chatscripts/default-script'))
    assert(modem._at_sockets_available == False)

def test_init_Ublox_chatscriptfileoverride(no_serial_port):
    modem = Ublox(chatscript_file='test-chatscript')
    assert(modem.timeout == 1)
    assert(modem.socket_identifier == 0)
    assert(modem.chatscript_file == 'test-chatscript')

# WRITE SOCKET

def test_socket_write_under_512(no_serial_port, override_command_result):
    modem = Ublox()
    data = '{message:{fill}{align}{width}}'.format(message='Test-', fill='@', align='<', width=64)
    modem.write_socket(data.encode())

def test_socket_write_over_512(no_serial_port, override_command_result):
    modem = Ublox()
    data = '{message:{fill}{align}{width}}'.format(message='Test-', fill='@', align='<', width=600)
    modem.write_socket(data.encode())