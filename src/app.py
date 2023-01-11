#!/usr/bin/env python3
from lib.ssh.client import SSHClientManager
from lib.adtran.mutables import RemoteDevice
from lib.adtran.util import AdtranUtil

client: SSHClientManager = SSHClientManager(auto_connect=True)

# Enable the enable mode
client.execute('enable')

# Retrieve a list of remote devices
rd_table = client.execute('show table remote-devices ont', True)

# Parse the remote device list
remote_devices = AdtranUtil.parse_remote_device_list(rd_table)

client.log.info('Remote Devices Table')

for device in list[RemoteDevice](remote_devices):
    client.log.info(f'Remote ID: {device.remote_index}; Serial Number: {device.serial_number}')

client.close()
