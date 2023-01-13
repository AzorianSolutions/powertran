import os
import time
from loguru import logger
from paramiko import AutoAddPolicy, Channel, SSHClient, Transport
from paramiko.ssh_exception import AuthenticationException


class ShellClientManagerException(Exception):
    pass


class SSHClientManager:
    _debug: bool = False
    _client: SSHClient | None = None
    _channel: Channel | None = None
    _host: str | None = None
    _port: int | None = None
    _username: str | None = None
    _password: str | None = None
    _known_hosts: str | None = None
    _receive_delay: float = 0.5
    _receive_wait_delay: float = 0.5

    @property
    def channel(self) -> Channel:
        """ Get the SSH channel. Instantiate one if it doesn't exist. Throw a ShellClientManagerException if client
        is not instantiated. """
        if not isinstance(self._client, SSHClient):
            raise ShellClientManagerException('SSH client is not instantiated')

        if not isinstance(self._channel, Channel):
            logger.debug('Opening SSH channel')
            self._channel = self._client.invoke_shell()

        return self._channel

    def __init__(self, host: str | None = None, port: int | None = None, username: str | None = None,
                 password: str | None = None, auto_connect: bool = False, known_hosts: str | None = None):
        """ Initialize the SSH client manager """

        Transport._preferred_keys = ('ssh-rsa',)
        Transport._preferred_pubkeys = ('ssh-rsa',)
        Transport._preferred_kex = ('diffie-hellman-group14-sha1', 'diffie-hellman-group1-sha1',)
        Transport._preferred_ciphers = ('aes128-cbc',)

        if isinstance(host, str):
            self._host = host

        if isinstance(port, int):
            self._port = port

        if isinstance(username, str):
            self._username = username

        if isinstance(password, str):
            self._password = password

        if known_hosts is None:
            self._known_hosts = os.getenv('PT_KNOWN_HOSTS', '~/.ssh/known_hosts')

        self._client = SSHClient()
        self._client.set_missing_host_key_policy(AutoAddPolicy())
        self._client.load_system_host_keys()

        if os.path.exists(self._known_hosts) and os.path.isfile(self._known_hosts):
            self._client.load_host_keys(self._known_hosts)

        if auto_connect:
            self.connect()

    def connect(self) -> bool:
        """ Connect to the SSH server """

        logger.debug(f'Connecting to {self._host} as {self._username}...')

        try:
            self._client.connect(self._host, username=self._username, password=self._password)
            return True
        except AuthenticationException as e:
            logger.critical(f'SSH Authentication Failed: {e}')
            return False

    def close(self) -> None:
        """ Close the SSH connection """
        logger.debug('Closing SSH connection')
        self._client.close()

    def execute(self, commands: str | list[str], process_more: bool = True) -> str:
        """ Execute one or more commands on the SSH server """

        logger.debug(f'Sending command' + ('s' if isinstance(commands, list) else '') + f' to {self._host}')

        if isinstance(commands, str):
            commands = [commands]

        stdout: str = ''

        # Execute each command one at a time and collect the output buffer before executing the next command
        for command in commands:
            # Wait until the channel is ready to send data
            while not self.channel.send_ready():
                pass

            # Encode the command
            encoded_command: bytes = f'{command}\n'.encode('utf-8')

            logger.debug(f'Sending {len(encoded_command)} byte command: {command}')

            # Send the command
            self.channel.send(encoded_command)

            # Wait for the command to complete and capture output
            stdout += self.get_buffer(process_more)

        return stdout

    def get_buffer(self, process_more: bool = False) -> str:
        """ Get the output buffer from the SSH server """
        stdout: str = ''

        while not self.channel.recv_ready():
            pass

        while True:
            if self.channel.recv_ready():
                stdout += self.channel.recv(65535).decode('utf-8')
                if process_more:
                    if stdout.splitlines()[-1].upper() == '--MORE--':
                        self.channel.send(' '.encode('utf-8'))
                        time.sleep(self._receive_delay)
                        continue
            else:
                time.sleep(self._receive_wait_delay)
                if not self.channel.recv_ready():
                    break

        return stdout
