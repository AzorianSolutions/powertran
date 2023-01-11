#!/usr/bin/env python3
from loguru import logger
from lib.adtran.api import AdtranAPI
from lib.adtran.util import AdtranUtil
from lib.powercode import EquipmentShapingData, PowercodeAPI

# Load the equipment shaping data from Powercode database
equipment: dict[str, EquipmentShapingData] = PowercodeAPI.get_equipment_shaping_data()

# Set up the Adtran API
adtran: AdtranAPI = AdtranAPI()

# Parse the remote device list from the Adtran device
devices = adtran.get_remote_devices()

# Build command buffer
commands: list[str] = AdtranUtil.build_command_buffer(equipment, devices)

logger.info('Applying shaping configuration to remote device')

# Execute the command buffer
result: str = adtran.execute(commands)

print(result)

logger.success('Shaping configuration applied successfully!')

# Disconnect from the device
adtran.close()
