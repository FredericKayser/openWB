#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusSerialClient


def detect_modbus_usb_port():
    """guess USB/modbus device name"""
    known_devices = ("/dev/ttyUSB0", "/dev/ttyACM0", "/dev/serial0")
    for device in known_devices:
        try:
            with open(device):
                return device
        except IOError:
            pass
    return known_devices[-1]  # this does not make sense, but is the same behavior as the old code


seradd = detect_modbus_usb_port()
idadd = int(sys.argv[2])

client = ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)
print("DUo2"+str(seradd)+"idadd"+str(idadd))
if (idadd < 100):
    # MPM3PM
    #resp = client.read_input_registers(0x0002,2, unit=idadd)
    #ikwh = resp.registers[1]
    resp = client.read_input_registers(0x0002, 4, unit=idadd)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
    ikwh = float(ikwh) / 100
    f = open('/var/www/html/openWB/ramdisk/llkwhs1', 'w')
    f.write(str(ikwh))
    f.close()

    resp = client.read_input_registers(0x0E, 2, unit=idadd)
    lla1 = resp.registers[1]
    lla1 = float(lla1) / 100
    f = open('/var/www/html/openWB/ramdisk/llas11', 'w')
    f.write(str(lla1))
    f.close()

    resp = client.read_input_registers(0x10, 2, unit=idadd)
    lla2 = resp.registers[1]
    lla2 = float(lla2) / 100
    f = open('/var/www/html/openWB/ramdisk/llas12', 'w')
    f.write(str(lla2))
    f.close()

    resp = client.read_input_registers(0x12, 2, unit=idadd)
    lla3 = resp.registers[1]
    lla3 = float(lla3) / 100
    f = open('/var/www/html/openWB/ramdisk/llas13', 'w')
    f.write(str(lla3))
    f.close()

    resp = client.read_input_registers(0x26, 2, unit=idadd)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
    if final < 10:
        final = 0
    f = open('/var/www/html/openWB/ramdisk/llaktuells1', 'w')
    f.write(str(final))
    f.close()

    resp = client.read_input_registers(0x08, 4, unit=idadd)
    voltage = resp.registers[1]
    voltage = float(voltage) / 10
    print("voltage1"+str(voltage))
    f = open('/var/www/html/openWB/ramdisk/llvs11', 'w')
    f.write(str(voltage))
    f.close()

    resp = client.read_input_registers(0x0A, 4, unit=idadd)
    voltage = resp.registers[1]
    voltage = float(voltage) / 10
    print("voltage2"+str(voltage))
    f = open('/var/www/html/openWB/ramdisk/llvs12', 'w')
    f.write(str(voltage))
    f.close()

    resp = client.read_input_registers(0x0C, 4, unit=idadd)
    voltage = resp.registers[1]
    voltage = float(voltage) / 10
    print("voltage3"+str(voltage))
    f = open('/var/www/html/openWB/ramdisk/llvs13', 'w')
    f.write(str(voltage))
    f.close()
else:
    # SDM630
    resp = client.read_input_registers(0x00, 2, unit=idadd)
    voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    voltage = float("%.1f" % voltage)
    f = open('/var/www/html/openWB/ramdisk/llvs11', 'w')
    f.write(str(voltage))
    f.close()
    resp = client.read_input_registers(0x06, 2, unit=idadd)
    lla1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
    lla1 = float("%.1f" % lla1)
    f = open('/var/www/html/openWB/ramdisk/llas11', 'w')
    f.write(str(lla1))
    f.close()
    resp = client.read_input_registers(0x08, 2, unit=idadd)
    lla2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
    lla2 = float("%.1f" % lla2)
    f = open('/var/www/html/openWB/ramdisk/llas12', 'w')
    f.write(str(lla2))
    f.close()
    resp = client.read_input_registers(0x0A, 2, unit=idadd)
    lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    lla3 = float("%.1f" % lla3)
    f = open('/var/www/html/openWB/ramdisk/llas13', 'w')
    f.write(str(lla3))
    f.close()
    resp = client.read_input_registers(0x0C, 2, unit=idadd)
    llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llw1 = int(llw1)
    resp = client.read_input_registers(0x0156, 2, unit=idadd)
    llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llkwh = float("%.3f" % llkwh)
    f = open('/var/www/html/openWB/ramdisk/llkwhs1', 'w')
    f.write(str(llkwh))
    f.close()
    resp = client.read_input_registers(0x0E, 2, unit=idadd)
    llw2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llw2 = int(llw2)
    resp = client.read_input_registers(0x10, 2, unit=idadd)
    llw3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llw3 = int(llw3)

    resp = client.read_input_registers(0x02, 2, unit=idadd)
    voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    voltage = float("%.1f" % voltage)
    f = open('/var/www/html/openWB/ramdisk/llvs12', 'w')
    f.write(str(voltage))
    f.close()
    resp = client.read_input_registers(0x04, 2, unit=idadd)
    voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    voltage = float("%.1f" % voltage)
    f = open('/var/www/html/openWB/ramdisk/llvs13', 'w')
    f.write(str(voltage))
    f.close()
    llg = llw1 + llw2 + llw3
    if llg < 10:
        llg = 0
    f = open('/var/www/html/openWB/ramdisk/llaktuells1', 'w')
    f.write(str(llg))
    f.close()
