from lib.mutables import Mutable


class RemoteDevice(Mutable):
    """ RemoteDevice Properties """
    _remote_index: str | None = None
    _admin_state: str | None = None
    _operational_state: str | None = None
    _serial_number: str | None = None
    _fiber_distance: str | None = None
    _ont_power: str | None = None
    _bip8: str | None = None
    _rdi: str | None = None
    _aes: str | None = None

    @property
    def serial_number(self) -> str | None:
        return self._serial_number.upper() if self._serial_number else None

    @serial_number.setter
    def serial_number(self, value: str | None):
        self._serial_number = value
