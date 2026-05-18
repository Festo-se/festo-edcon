from edcon.utils.logging import Logging
from edcon.edrive.parameter_set import ParameterSet
from edcon.edrive.parameter_handler import ParameterHandler
from edcon.edrive.com_modbus import ComModbus

# Enable loglevel info
Logging()

com = ComModbus("192.168.0.1")

parameter_set = ParameterSet("my_parameters.pck")
parameter_handler = ParameterHandler(com)

i = None
for i, parameter in enumerate(parameter_set):
    status = parameter_handler.write(parameter)

    if not status:
        Logging.logger.error(f"Setting {parameter.uid()} to {parameter.value} failed")

print(f"{i+1} PNUs succesfully written!")
