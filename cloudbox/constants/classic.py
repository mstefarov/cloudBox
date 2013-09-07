# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

FORMAT_LENGTHS = {
    "b": 1,
    "a": 1024,
    "s": 64,
    "h": 2,
    "i": 4,
}

TYPE_INITIAL = 0
TYPE_KEEPALIVE = 1
TYPE_PRECHUNK = 2
TYPE_CHUNK = 3
TYPE_LEVELSIZE = 4
TYPE_BLOCKCHANGE = 5
TYPE_BLOCKSET = 6
TYPE_SPAWNPOINT = 7
TYPE_PLAYERPOS = 8
TYPE_NINE = 9
TYPE_TEN = 10
TYPE_PLAYERDIR = 11
TYPE_PLAYERLEAVE = 12
TYPE_MESSAGE = 13
TYPE_ERROR = 14
TYPE_SETPERM = 15

from cloudbox.common.format import *

TYPE_FORMATS = {
    TYPE_INITIAL: Format("bssb"),
    TYPE_KEEPALIVE: Format(""),
    TYPE_PRECHUNK: Format(""),
    TYPE_CHUNK: Format("hab"),
    TYPE_LEVELSIZE: Format("hhh"),
    TYPE_BLOCKCHANGE: Format("hhhbb"),
    TYPE_BLOCKSET: Format("hhhb"),
    TYPE_SPAWNPOINT: Format("bshhhbb"),
    TYPE_PLAYERPOS: Format("bhhhbb"),
    TYPE_NINE: Format("bbbbbb"),
    TYPE_TEN: Format("bbbb"),
    TYPE_PLAYERDIR: Format("bbb"),
    TYPE_PLAYERLEAVE: Format("b"),
    TYPE_MESSAGE: Format("bs"),
    TYPE_ERROR: Format("s"),
    TYPE_SETPERM: Format("bb")
}