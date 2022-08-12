"""
Contains current built-in EDriveModbus flavour definitions.
"""
from edrive.modbus_flavours.behavior_cmmt_as import BehaviorCmmtAs

reg_cmmt_as = {"pd_in": 100, "pd_out": 0, "timeout": 400}
reg_cpx_ap = {"pd_in": 5000, "pd_out": 0, "timeout": 14000}

flavours = {"CMMT-AS": {"registers": reg_cmmt_as, "behavior": BehaviorCmmtAs},
            "CPX-AP": {"registers": reg_cpx_ap}}
