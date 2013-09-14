# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from cloudbox.constants.classic import Format

TYPE_EXTINFO = 16
TYPE_EXTENTRY = 17

TYPE_FORMATS = {
    TYPE_EXTINFO: Format("sh"),
    TYPE_EXTENTRY: Format("si"),
}
