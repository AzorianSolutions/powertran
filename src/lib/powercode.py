from lib.mutables import Mutable
from lib.mysql import MySQLClient


class EquipmentShapingData(Mutable):
    """ A mutable class for storing Powercode equipment shaping data. """

    _serial: str = None
    _downstream: int = None
    _upstream: int = None


class PowercodeAPI:

    @staticmethod
    def get_equipment_shaping_data() -> dict[str, EquipmentShapingData]:
        """ Return a dictionary of equipment shaping data keyed by serial number. """

        # Load the equipment shaping data SQL query from a file
        sql: str = open('src/sql/equipment-shaping-data.sql', 'r').read()

        # Execute the loaded query against the database
        c = MySQLClient.db().cursor()
        c.execute(sql)

        # Structure results into a dictionary of EquipmentShapingData objects
        return {row['serial']: EquipmentShapingData(**row) for row in c.fetchall()}
