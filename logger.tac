from twisted.application.service import Application

from cloudbox.common.service import cloudBoxService
from cloudbox.common.constants import *

service = cloudBoxService("CentralLogger")
application = Application("cloudBox")
service.setServiceParent(application)