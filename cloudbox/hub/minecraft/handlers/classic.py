# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

import hashlib

from cloudbox.common.handlers import BasePacketHandler
from cloudbox.constants.classic import *

class HandshakePacketHandler(BasePacketHandler):
    """
    A Handler class for Login requests.
    """

    @staticmethod
    def handleData(data):
        # Get the client's details
        protocol, self.username, mppass, utype = data
        if self.parent.identified == True:
            self.factory.logger.info("Kicked '%s'; already logged in to server" % (self.username))
            self.sendError("You already logged in!")
        # Right protocol?
        if protocol != 7:
            self.sendError("Wrong protocol.")
            break
        # Check their password
        correct_pass = hashlib.md5(self.factory.salt + self.username).hexdigest()[-32:].strip("0")
        mppass = mppass.strip("0")
        if not self.transport.getHost().host.split(".")[0:2] == self.ip.split(".")[0:2]:
            if mppass != correct_pass:
                self.factory.logger.info(
                    "Kicked '%s'; invalid password (%s, %s)" % (self.username, mppass, correct_pass))
                self.sendError("Incorrect authentication, please try again.")
                return
        value = self.factory.runHook("prePlayerConnect", {"client": self})
        if not value and value != None: return
        self.factory.logger.info("Connected, as '%s'" % self.username)
        self.identified = True
        # Are they banned?
        if self.factory.isBanned(self.username):
            self.sendError("You are banned: %s" % self.factory.banReason(self.username))
            return
        # OK, see if there's anyone else with that username
        if not self.factory.duplicate_logins and self.username.lower() in self.factory.usernames:
            self.factory.usernames[self.username.lower()].sendError("You logged in on another computer.")
        self.factory.usernames[self.username.lower()] = self
        self.factory.joinWorld(self.factory.default_name, self)
        # Send them back our info.
        self.sendPacked(
            TYPE_INITIAL,
            7, # Protocol version
            packString(self.factory.server_name),
            packString(self.factory.server_message),
            100 if (self.isOp() if hasattr(self, "world") else False) else 0,
        )
        # Then... stuff
        for client in self.factory.usernames.values():
            client.sendServerMessage("%s has come online." % self.username)
        if self.factory.irc_relay:
            self.factory.irc_relay.sendServerMessage("07%s has come online." % self.username)
        reactor.callLater(0.1, self.sendLevel)
        reactor.callLater(1, self.sendKeepAlive)
        self.factory.runHook("onPlayerConnect", {"client": self}) # Run the player connect hook

    @staticmethod
    def packData(data):
        pass


class KeepAlivePacketHandler(BasePacketHandler):
    """
    A Handler class for Keep Alives.
    """

    @staticmethod
    def packData(data):
        return TYPE_FORMATS[TYPE_KEEPALIVE].encode(TYPE_KEEPALIVE)


class LevelInitPacketHandler(BasePacketHandler):
    """
    A Handler class for Level Initialization.
    """

    @staticmethod
    def packData(data):


class LevelChunkPacketHandler(BasePacketHandler):
    """
    A Handler class for Level Chunks.
    """

    @staticmethod
    def packData(data):


class LevelFinalizePacketHandler(BasePacketHandler):
    """
    A Handler class for Level Finalization.
    """

    @staticmethod
    def packData(data):

class BlockChangePacketHandler(BasePacketHandler):
    """
    A Handler class for Block Changes.
    """

    @staticmethod
    def handleData():


class BlockSetPacketHandler(BasePacketHandler):
    """
    A Handler class for Setting a Block.
    """

    @staticmethod
    def packData(data):


class SpawnPlayerPacketHandler(BasePacketHandler):
    """
    A Handler class for player spawning.
    """

    @staticmethod
    def packData(data):


class PlayerPosPacketHandler(BasePacketHandler):
    """
    A Handler class for player position updates.
    """

    @staticmethod
    def handleData(data):


    def packData(data):


class PlayerOrtPacketHandler(BasePacketHandler):
    """
    A Handler class for player orientation updates.
    """

    @staticmethod
    def packData(data):


class PlayerDespawnPacketHandler(BasePacketHandler):
    """
    A Handler class for player despawning.
    """

    @staticmethod
    def packData(data):
        return TYPE_FORMATS[TYPE_PLAYERDESPAWN].encode(TYPE_PLAYERDESPAWN, data["playerID"])


class MessagePacketHandler(BasePacketHandler):
    """
    A Handler class for messages.
    """

    @staticmethod
    def handleData(data):


    @staticmethod
    def packData(data):


class ErrorPacketHandler(BasePacketHandler):
    """
    A Handler class for error messages.
    """

    @staticmethod
    def packData(data):


class SetUserTypePacketHandler(BasePacketHandler):
    """
    A Handler for setting op permissions.
    """

    @staticmethod
    def packData(data):

