# this is the file that gets snmp data from devices. "and tells if they are responding or not"
from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity
from pysnmp.hlapi import *


def snmp_get(ip, community, oid, timeout=1, retries=1):
    """Perform SNMP GET and return value as string or None."""
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),  # SNMPv1
        UdpTransportTarget((ip, 161), timeout=timeout, retries=retries),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication or errorStatus:
        return None

    for varBind in varBinds:
        return str(varBind[1])
