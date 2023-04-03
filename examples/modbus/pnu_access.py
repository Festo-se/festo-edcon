from edrive.edrive_modbus import EDriveModbus
from edrive.edrive_logging import EDriveLogging

# Enable loglevel info
EDriveLogging()

edrive = EDriveModbus('192.168.0.51')

# Read currently selected telegram
original_value = edrive.read_pnu(3490, 0, 'H')

# Configure a different telegram
new_value = 1 if not original_value == 1 else 111
edrive.write_pnu(3490, 0, new_value, 'H')

# Write back original value
edrive.write_pnu(3490, 0, original_value, 'H')
