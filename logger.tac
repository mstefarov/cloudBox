# cloudBox is copyright 2012 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from twisted.application.service import Application

from cloudbox.common.service import cloudBoxService
from cloudbox.common.constants import *

service = cloudBoxService("CentralLogger")
application = Application("cloudBox")
service.setServiceParent(application)