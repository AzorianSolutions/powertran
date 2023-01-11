#!/usr/bin/env python3
from lib.ssh.client import SSHClientManager
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
devices = AdtranUtil.parse_remote_device_list(rd_table)

# Build command buffer
commands: list[str] = AdtranUtil.build_command_buffer(equipment, devices)

client.log.info('Applying shaping configuration to remote device')

# Execute the command buffer
result: str = client.execute('\r'.join(commands))

print(result)

client.log.success('Shaping configuration applied successfully!')

# Disconnect from the device
client.close()
