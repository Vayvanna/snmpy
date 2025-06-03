from pysnmp.hlapi import (
    getCmd, SnmpEngine, CommunityData,
    UdpTransportTarget, ContextData,
    ObjectType, ObjectIdentity
)

def snmp_get(ip, community, oid, port=161, timeout=1, retries=1):
    """Perform SNMP GET and return value as string or None if invalid."""
    # print(f"{ip} is of type {type(ip)}")
    # print(f"{port} is of type {type(port)}")
    # print(f"{community} is of type {type(community)}")
    # hard coded community, ip & port.
    iterator = getCmd(
        SnmpEngine(),
        CommunityData("public", mpModel=0),  # SNMPv1
        UdpTransportTarget(("127.0.0.1", 1161), timeout=timeout, retries=retries),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication or errorStatus:
        # print("line 26 helpersofsn.py")
        return None

    for varBind in varBinds:
        value = str(varBind[1])
        if value.strip() in ["", "No Such Object currently exists", "No Such Instance currently exists"]:
            return None
        # print(f"[DEBUG] SNMP GET {ip}:{port} {oid} → {value}")
        return value

# def snmp_get(ip, community, oid, port=161, timeout=1, retries=1):
#     """Perform SNMP GET and return value as string or None."""
#     iterator = getCmd(
#         SnmpEngine(),
#         CommunityData(community, mpModel=0),  # SNMPv1
#         UdpTransportTarget((ip, port), timeout=timeout, retries=retries),
#         ContextData(),
#         ObjectType(ObjectIdentity(oid))
#     )

#     errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

#     if errorIndication or errorStatus:
#         return None

#     for varBind in varBinds:
#         return str(varBind[1])




#ماذا عن 127.0.0.1؟ هل يجب أن أحفظ ذلك في قناة PY Simulator؟