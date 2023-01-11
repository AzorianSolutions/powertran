import re
from loguru import logger
from re import Pattern
from lib.adtran.mutables import RemoteDevice


class AdtranUtil:
    """ AdtranUtil Properties """
    _remote_id_pattern: Pattern = re.compile(r'^[0-9]{1,3}@(?:[0-9]){1,3}/(?:[0-9]){1,3}/(?:[0-9]){1,3}\.?[gpon]{0,4}$')
    _serial_number_pattern: Pattern = re.compile(r'^(ADTN|UBNT)[a-z0-9]{8}$')
    _rd_table_columns: list[str] = ['remote_index', 'admin_state', 'operational_state', 'serial_number',
                                               'fiber_distance', 'ont_power', 'bip8', 'rdi', 'aes']

    """ AdtranUtil Methods """

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
