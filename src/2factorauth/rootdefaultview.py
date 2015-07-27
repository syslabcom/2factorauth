from zope.browserpage import ViewPageTemplateFile
from zope.formlib import form


class RootDefaultView(form.DisplayForm):

    __call__ = ViewPageTemplateFile('rootdefaultview.pt')
