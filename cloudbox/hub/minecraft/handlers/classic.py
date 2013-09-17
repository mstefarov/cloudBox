# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import hashlib

from twisted.internet.task import LoopingCall

from cloudbox.common.handlers import BasePacketHandler
from cloudbox.common.util import packString
from cloudbox.constants.common import *
from cloudbox.constants.classic import *


class HandshakePacketHandler(BasePacketHandler):
    """
    A Handler class for Login requests.
    """

    @staticmethod
    def handleData(data):
        # Get the client's details
        protocol, data["parent"].username, mppass, utype = data["packetData"]
        if data["parent"].identified:
            # Sent two login packets - I wonder why?
            data["parent"].factory.logger.info("Kicked '%s'; already logged in to server" % (data["parent"].username))
            data["parent"].sendError("You already logged in!")

        # Right protocol?
        if protocol != 7:
            data["parent"].sendError("Wrong protocol.")
            return

        # Check their password
        expectedPassword = hashlib.md5(data["parent"].factory.salt + data["parent"].username).hexdigest()[-32:].strip("0")
        mppass = mppass.strip("0")
        # TODO: Rework this - possibly limit to localhost only?
        #if not data["parent"].transport.getHost().host.split(".")[0:2] == data["parent"].ip.split(".")[0:2]:
        if mppass != expectedPassword:
            data["parent"].factory.logger.info(
                "Kicked '%s'; invalid password (%s, %s)" % (data["parent"].username, mppass, expectedPassword))
            data["parent"].sendError("Incorrect authentication, please try again.")
            return
        #value = data["parent"].factory.runHook("prePlayerConnect", {"client": self})

        # Are they banned?
        bans = data["parent"].factory.getBans(data["parent"].username, data["parent"].ip)
        if bans:
            data["parent"].sendError("You are banned: %s" % bans[-1]["reason"])
            return

        # OK, see if there's anyone else with that username
        if data["parent"].username.lower() in data["parent"].factory.usernames:
            data["parent"].factory.usernames[data["parent"].username.lower()].sendError(
                "You logged in on another computer.", dontDisconnect=true)
            data["parent"].transport.loseConnection() # Terminate now to avoid problems when switching protocol objects
        data["parent"].factory.usernames[data["parent"].username.lower()] = self

        # All check complete. Request World Server to prepare level
        data["parent"].factory.joinDefaultWorld(data["parent"])

        # Announce our presence
        data["parent"].identified = True
        data["parent"].factory.logger.info("Connected, as '%s'" % data["parent"].username)
        #for client in data["parent"].factory.usernames.values():
        #    client.sendServerMessage("%s has come online." % data["parent"].username)

        # Send them back our info.
        # TODO: CPE
        #if data["parent"].factory.settings["main"]["enable-cpe"]:
        #    data["parent"].sendPacket(TYPE_EXTINFO, len(data["parent"].cpeExtensions)

        data["parent"].sendPacket(TYPE_INITIAL, [
            7, # Protocol version
            packString(data["parent"].factory.settings["main"]["name"]),
            packString(data["parent"].factory.settings["main"]["motd"]),
            #100 if (self.isOp() if hasattr(self, "world") else False) else 0, # TODO
            0
        ])
        data["parent"].loops.registerLoop("keepAlive", LoopingCall(data["parent"].sendKeepAlive).start(1))
        #data["parent"].factory.runHook("onPlayerConnect", {"client": data["parent"]}) # Run the player connect hook

    @staticmethod
    def unpackData(data):
        print(data)
        return TYPE_FORMATS[TYPE_LEVELDATA].decode(data)

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_INITIAL])


class KeepAlivePacketHandler(BasePacketHandler):
    """
    A Handler class for Keep Alives.
    """

    @staticmethod
    def packData(data):
        return ""

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_KEEPALIVE])


class LevelInitPacketHandler(BasePacketHandler):
    """
    A Handler class for Level Initialization.
    """

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_LEVELINIT])


class LevelDataPacketHandler(BasePacketHandler):
    """
    A Handler class for Level Chunks.
    """

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_LEVELDATA])


class LevelFinalizePacketHandler(BasePacketHandler):
    """
    A Handler class for Level Finalization.
    """

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_LEVELFINALIZE])


class BlockChangePacketHandler(BasePacketHandler):
    """
    A Handler class for Block Changes.
    """

    @staticmethod
    def handleData(data):
        if data["_serverType"] == SERVER_TYPES["WorldServer"]:
            x, y, z, created, block = data["packetData"]
            if not data["parent"].identified:
                data["parent"].factory.logger.info(
                    "Kicked '%s'; did not send a login before building" % data["parent"].ip)
                data["parent"].sendError("Provide an authentication before building.")
                return
            if block == 255:
                # Who sends 255 anyway?
                data["parent"].factory.logger.debug("%s sent block 255 as 0" % data["parent"].username)
                block = 0
            # Check if out of block range or placing invalid blocks
            if block not in BLOCKS.keys() or block in [BLOCKS_BY_NAME["water"], BLOCKS_BY_NAME["lava"]]:
                data["parent"].factory.logger.info("Kicked '%s' (IP %s); Tried to place invalid block %s" % (
                                        data["parent"].username, data["parent"].ip, block))
                data["parent"].sendError("Invalid blocks are not allowed!")
                return
            # TODO Permission Manager
            if block == 7:  # and not permissionManager.hasWorldPermission(data["parent"].permissions):
                data["parent"].factory.logger.info("Kicked '%s'; Tried to place bedrock." % data["parent"].ip)
                data["parent"].sendError("Don't build bedrocks!")
                return
            try:
            # If we're read-only, reverse the change
                allowBuilding = data["parent"].factory.runHook(
                    "onBlockClick",
                    {"x": x, "y": y, "z": z, "block": block, "client": data["parent"]}
                )
                if not allowBuilding:
                    data["parent"].sendBlock(x, y, z)
                    return
                # Track if we need to send back the block change
                overridden = False
                selectedBlock = block
                # If we're deleting, block is actually air
                # (note the selected block is still stored as selectedBlock)
                if not created:
                    block = 0
                # Pre-hook, for stuff like /paint
                new_block = data["parent"].factory.runHook("preBlockChange",
                    {"x": x, "y": y, "z": z, "block": block, "selected_block": selectedBlock, "client": data["parent"]})
                if new_block is not None:
                    block = new_block
                    overridden = True
                # Block detection hook that does not accept any parameters
                data["parent"].factory.runHook(
                    "blockDetect",
                    {"x": x, "y": y, "z": z, "block": block, "client": data["parent"]}
                )
                # Call hooks
                new_block = data["parent"].factory.runHook(
                    "blockChange",
                    {"x": x, "y": y, "z": z, "block": block, "selected_block": selectedBlock, "client": data["parent"]}
                )
                if new_block is False:
                    # They weren't allowed to build here!
                    data["parent"].sendBlock(x, y, z)
                    return
                # TODO Use object as hint
                elif new_block == -1:
                    # Someone else handled building, just continue
                    return
                elif new_block is not None:
                    if not new_block:
                        block = new_block
                        overridden = True
                # OK, save the block
                data["parent"].world[x, y, z] = chr(block)
                # Now, send the custom block back if we need to
                if overridden:
                    data["parent"].sendBlock(x, y, z, block)
            # Out of bounds!
            except (KeyError, AssertionError):
                data["parent"].sendPacket(TYPE_BLOCKSET, x, y, z, "\0")
            # OK, replay changes to others
            else:
                data["packetData"].factory.queue.put((data["parent"], TASK_BLOCKSET, (x, y, z, block)))
        else:
            # Hand it over to the WorldServer
            data["parent"].factory.relayMCPacketToWorldServer(TYPE_BLOCKCHANGE, data["packetData"])

    @staticmethod
    def unpackData(data):
        return TYPE_FORMATS[TYPE_BLOCKCHANGE].decode(data)

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_BLOCKCHANGE])


class BlockSetPacketHandler(BasePacketHandler):
    """
    A Handler class for Setting a Block.
    """

    @staticmethod
    def unpackData(data):
        return TYPE_FORMATS[TYPE_BLOCKSET].decode(data)

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_BLOCKSET])


class SpawnPlayerPacketHandler(BasePacketHandler):
    """
    A Handler class for player spawning.
    """

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_SPAWNPLAYER])

class PlayerPosPacketHandler(BasePacketHandler):
    """
    A Handler class for player position updates.
    """

    @staticmethod
    def handleData(data):
        pass

    @staticmethod
    def unpackData(data):
        return TYPE_FORMATS[TYPE_PLAYERPOS].decode(data)

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_PLAYERPOS])


class PlayerOrtPacketHandler(BasePacketHandler):
    """
    A Handler class for player orientation updates.
    """

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_PLAYERORT])


class PlayerDespawnPacketHandler(BasePacketHandler):
    """
    A Handler class for player despawning.
    """

    @staticmethod
    def packData(data):
        return TYPE_FORMATS[TYPE_PLAYERDESPAWN].encode(data["playerID"])

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_PLAYERDESPAWN])


class MessagePacketHandler(BasePacketHandler):
    """
    A Handler class for messages.
    """

    @staticmethod
    def handleData(data):
        pass

    @staticmethod
    def unpackData(data):
        return TYPE_FORMATS[TYPE_MESSAGE].decode(data)

    @staticmethod
    def packData(data):
        pass

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_MESSAGE])


class ErrorPacketHandler(BasePacketHandler):
    """
    A Handler class for error messages.
    """

    @staticmethod
    def packData(data):
        return TYPE_FORMATS[TYPE_ERROR].encode(data["error"])

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_ERROR])


class SetUserTypePacketHandler(BasePacketHandler):
    """
    A Handler for setting op permissions.
    """

    @staticmethod
    def getExpectedLength():
        return len(TYPE_FORMATS[TYPE_SETUSERTYPE])
