import re
from loguru import logger
from re import Pattern
from lib.adtran.mutables import RemoteDevice
from lib.powercode import EquipmentShapingData


class AdtranUtil:
    """ A utility class for Adtran devices. """

    _remote_id_pattern: Pattern = re.compile(r'^[0-9]{1,3}@[0-9]{1,3}/[0-9]{1,3}/[0-9]{1,3}\.?[gpon]{0,4}$', re.I)
    _serial_number_pattern: Pattern = re.compile(r'^(?:ADTN|UBNT)[a-z0-9]{8}$', re.I)
    _rd_table_columns: list[str] = ['remote_index', 'admin_state', 'operational_state', 'serial_number',
                                    'fiber_distance', 'ont_power', 'bip8', 'rdi', 'aes']

    @staticmethod
    def parse_remote_device_list(source: str) -> list[RemoteDevice]:
        """
        Parse the remote device list into a list of RemoteDevice objects
        :param source: The remote device list to parse
        :return: A list of RemoteDevice objects
        """
        devices: list[RemoteDevice] = []
        lines = source.splitlines()

        for line in lines:
            # Split the line into columns
            columns: list[str] = line.split()

            # Skip rows without the proper number of columns
            if len(columns) != 9:
                continue

            # Test the remote ID column value for validity
            if not AdtranUtil._remote_id_pattern.match(columns[0]):
                logger.debug(f'Invalid Remote ID: {columns[0]}')
                continue

            # Test the serial number column value for validity
            if not AdtranUtil._serial_number_pattern.match(columns[3]):
                logger.debug(f'Invalid Serial Number: {columns[3]}')
                continue

            # Re-format the remote ID column value to deal with CLI trimming
            columns[0] = columns[0].split('.')[0] + '.gpon'

            # Create a new RemoteDevice object
            props: dict[str, str] = {AdtranUtil._rd_table_columns[i]: columns[i] for i in range(0, len(columns))}
            device: RemoteDevice = RemoteDevice(**props)
            devices.append(device)

        return devices

    @staticmethod
    def build_shaping_buffer(equipment: dict[str, EquipmentShapingData], devices: list[RemoteDevice]) -> list[str]:
        """
        Build the command buffer to apply shaping configuration to remote devices
        :param equipment: A dictionary of EquipmentShapingData objects
        :param devices: A list of RemoteDevice objects
        """
        commands: list[str] = ['enable', 'config t']

        for device in list[RemoteDevice](devices):
            if device.serial_number not in equipment:
                logger.warning(f'No equipment shaping data found for {device.serial_number}')
                continue

            esd: EquipmentShapingData = equipment[device.serial_number]
            id_parts: list[str] = device.remote_index.split('@')
            index: int = int(id_parts[0])
            location: str = id_parts[1]
            location_parts: list[str] = location.split('.')[0].split('/')
            shelf: int = int(location_parts[0])
            slot: int = int(location_parts[1])

            logger.debug(f'Remote ID: {device.remote_index}; Serial Number: {device.serial_number}; '
                         + f'Downstream: {esd.downstream}; Upstream: {esd.upstream}')

            commands.append(f'shaper “interface gpon {index}/0/1@{location} channel 1” {device.remote_index}')
            commands.append(f'rate {esd.downstream}')
            commands.append('exit')

            commands.append(f'shaper “remote-device {device.remote_index}_0” {shelf}/{slot}')
            commands.append(f'rate {esd.upstream}')
            commands.append('exit')

        commands.append('exit')
        commands.append('exit')

        return commands
