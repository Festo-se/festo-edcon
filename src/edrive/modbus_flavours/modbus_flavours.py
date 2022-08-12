"""
Contains current built-in EDriveModbus flavour definitions.
"""
from edrive.modbus_flavours.flavour_cmmt_as import FlavourCmmtAs
from edrive.modbus_flavours.flavour_cpx_ap import FlavourCpxAp


def modbus_flavours():
    """
    Function that returns a dict with all build-in EDriveModbus flavours

    Currently built-in flavours:
        - ``'CMMT-AS'``
        - ``'CPX-AP'``
    """
    return {"CMMT-AS": FlavourCmmtAs, "CPX-AP": FlavourCpxAp}
