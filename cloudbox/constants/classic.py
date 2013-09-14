# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.common.format import Format

TYPE_INITIAL = 0
TYPE_KEEPALIVE = 1
TYPE_LEVELINIT = 2
TYPE_LEVELDATA = 3
TYPE_LEVELFINALIZE = 4
TYPE_BLOCKCHANGE = 5
TYPE_BLOCKSET = 6
TYPE_SPAWNPLAYER = 7
TYPE_PLAYERPOS = 8
TYPE_PLAYERORT = 11
TYPE_PLAYERDESPAWN = 12
TYPE_MESSAGE = 13
TYPE_ERROR = 14
TYPE_SETUSERTYPE = 15

TYPE_FORMATS = {
    TYPE_INITIAL: Format("bssb"),
    TYPE_KEEPALIVE: Format(""),
    TYPE_LEVELINIT: Format(""),
    TYPE_LEVELDATA: Format("hab"),
    TYPE_LEVELFINALIZE: Format("hhh"),
    TYPE_BLOCKCHANGE: Format("hhhbb"),
    TYPE_BLOCKSET: Format("hhhb"),
    TYPE_SPAWNPLAYER: Format("bshhhbb"),
    TYPE_PLAYERPOS: Format("bhhhbb"),
    TYPE_PLAYERORT: Format("bbb"),
    TYPE_PLAYERDESPAWN: Format("b"),
    TYPE_MESSAGE: Format("bs"),
    TYPE_ERROR: Format("s"),
    TYPE_SETUSERTYPE: Format("bb")
}