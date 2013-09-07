# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.application.service import Application

from cloudbox.common.service import cloudBoxService
from cloudbox.constants import *

service = cloudBoxService("HubServer")
application = Application("cloudBox")
service.setServiceParent(application)