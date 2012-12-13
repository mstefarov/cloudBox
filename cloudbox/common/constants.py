# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

# Server types

SERVER_TYPES = {
    "HubServer": 0,
    "WorldServer": 1,
    "DatabaseServer": 2,
    "CentralLogger": 3,
    "HeartbeatService": 4,
}

SERVER_TYPES_INV = dict((v, k) for k, v in SERVER_TYPES.iteritems())

DEFAULT_PERMISSIONS = {

}

# Handlers - the basics

# Packets sent from clients
HANDLERS_CLIENT_BASIC = {
    0x00: ["keepAlive", "cloudbox.common.handlers"],
    0x01: ["initHandshake", "cloudbox.common.handlers"],
    0x02: ["handshakeEncryptResponse", "cloudbox.common.handlers"], # Placeholder for encryption, unused for now
    0xFF: ["disconnect", "cloudbox.common.handlers"],
}

# Packets sent from servers
HANDLERS_SERVER_BASIC = {
    0x00: ["keepAlive", "cloudbox.common.handlers"],
    0x01: ["handshakeEncrypt", "cloudbox.common.handlers"], # Placeholder for encryption, unused for now
    0x02: ["establishConnection", "cloudbox.common.handlers"],
    0xFF: ["disconnect", "cloudbox.common.handlers"],
}

# Errors

ERR_NOT_ENOUGH_DATA = 100
ERR_METHOD_NOT_FOUND = 101
ERR_UNABLE_TO_PARSE_DATA = 102