#!/usr/bin/env python3
from lib.ssh.client import SSHClientManager
from lib.adtran.mutables import RemoteDevice
from lib.adtran.util import AdtranUtil
from lib.powercode import EquipmentShapingData, PowercodeAPI

# Load the equipment shaping data from Powercode database
equipment: dict[str, EquipmentShapingData] = PowercodeAPI.get_equipment_shaping_data()

# Set up the SSH client
client: SSHClientManager = SSHClientManager(auto_connect=True)

# Enable the enable mode
client.execute('enable')

# Retrieve a list of remote devices
rd_table = client.execute('show table remote-devices ont', True)

# Parse the remote device list
remote_devices = AdtranUtil.parse_remote_device_list(rd_table)

# Build command buffer
commands: list[str] = []

for device in list[RemoteDevice](remote_devices):
    client.log.info(f'Remote ID: {device.remote_index}; Serial Number: {device.serial_number}')
    # TODO: Build command buffer

# TODO: Apply command buffer to device

client.close()
