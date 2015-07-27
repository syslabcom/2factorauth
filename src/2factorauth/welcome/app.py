from zope.interface import implements
from zope.site.folder import Folder

from interfaces import ISampleApplication


class SampleApplication(Folder):

    implements(ISampleApplication)
    name = u""
    description = u""
