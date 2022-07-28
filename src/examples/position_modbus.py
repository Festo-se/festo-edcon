from cmmt.cmmt_modbus import CmmtModbus
from cmmt.cmmt_position_function_block import CmmtPositionFunctionBlock

cmmt_driver = CmmtModbus('192.168.0.51')
with CmmtPositionFunctionBlock(cmmt_driver) as pos_block:
    pos_block.request_plc_control()
    pos_block.acknowledge_faults()
    pos_block.enable_powerstage()
    pos_block.homing_task()
    pos_block.position_task(10000, 600000)
    pos_block.position_task(-5000, 50000)
    pos_block.position_task(30000, 600000, absolute=True)
