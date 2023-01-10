#!/usr/bin/env python3
from lib.ssh.client import SSHClientManager

client: SSHClientManager = SSHClientManager(auto_connect=True)

# Enable the enable mode
client.execute('enable')

# Retrieve a list of remote devices
remote_devices_table = client.execute('show table remote-devices ont', True)

client.log.info('Remote Devices Table')
print(remote_devices_table)

client.close()
