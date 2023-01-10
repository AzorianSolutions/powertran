#!/usr/bin/env python3
import os
import paramiko
import pprint
from paramiko import AutoAddPolicy, Channel, ChannelException, SSHClient, Transport
from paramiko.ssh_exception import AuthenticationException

host: str = os.getenv('PT_HOST', '127.0.0.1')
username: str = os.getenv('PT_USERNAME', 'ADMIN')
password: str = os.getenv('PT_PASSWORD', None)
known_hosts_path: str = os.getenv('PT_KNOWN_HOSTS', '~/.ssh/known_hosts')

paramiko.Transport._preferred_keys = ('ssh-rsa', )
paramiko.Transport._preferred_pubkeys = ('ssh-rsa', )
paramiko.Transport._preferred_kex = ('diffie-hellman-group14-sha1', 'diffie-hellman-group1-sha1', )
paramiko.Transport._preferred_ciphers = ('aes128-cbc', )


def get_shell_buffer(channel: Channel) -> str:
    buffer: str = ''
    empty: bool = False

    while not channel.recv_ready():
        pass

    while not empty:
        data: str = channel.recv(1024).decode('utf-8')
        if not len(data):
            empty = True
            break
        buffer += data

    return buffer


client = SSHClient()
client.load_system_host_keys()

if os.path.exists(known_hosts_path) and os.path.isfile(known_hosts_path):
    client.load_host_keys(known_hosts_path)

client.set_missing_host_key_policy(AutoAddPolicy())

try:
    print(f'Connecting to {host} as {username}...')
    client.connect(host, username=username, password=password)

    buffer: str = ''
    shell: Channel = client.invoke_shell(width=800, height=600)

    if shell.send_ready():
        shell.send('enable\r'.encode('utf-8'))
        shell.send('show table remote-devices ont\r'.encode('utf-8'))

    buffer += get_shell_buffer(shell)

    while shell.recv_ready():
        buffer += shell.recv(1024).decode('utf-8')

    # while recv := shell.recv(100).decode('utf-8'):
    #     buffer += recv

    print(buffer)
    print('TEST TEST TEST')

except AuthenticationException as e:
    print(f'Authentication failed: {e}')

client.close()
