from zope.interface import implements
from zope.site.folder import Folder

from interfaces import ITwoFactorApplication


class TwoFactorApplication(Folder):

    implements(ITwoFactorApplication)
    name = u""
    description = u""
