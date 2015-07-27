from zope.site.interfaces import IFolder
from zope.schema import TextLine
from zope.schema import Text

class ISampleApplication(IFolder):
    """The main application container."""

    name = TextLine(
        title=u"Name",
        description=u"Name of application.",
        default=u"",
        required=True)

    description = Text(
        title=u"Description",
        description=u"The name of application container.",
        default=u"",
        required=False)
