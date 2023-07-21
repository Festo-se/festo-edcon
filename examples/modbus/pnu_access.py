from edcon.edrive.com_modbus import ComModbus
from edcon.utils.logging import Logging

# Enable loglevel info
Logging()

com = ComModbus('192.168.0.1')

# Read currently selected telegram
original_value = com.read_pnu(3490, 0)

# Configure a different telegram
new_value = 1 if not original_value == 1 else 111
com.write_pnu(3490, 0, new_value)

# Write back original value
com.write_pnu(3490, 0, original_value)
