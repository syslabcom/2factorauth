from zope.browserpage import ViewPageTemplateFile
from zope.formlib import form
from recaptcha.client.captcha import displayhtml

PUBKEY = "6LcGPQ4TAAAAAMdi8fy5CnG7F6esK2wVErabJojk"


class RootDefaultView(form.DisplayForm):

    index = ViewPageTemplateFile('templates/rootdefaultview.pt')

    def __call__(self):
        return self.index()


class LoginFormView(form.DisplayForm):

    index = ViewPageTemplateFile('templates/login_form.pt')

    def __call__(self):
        return self.index()


class TanFormView(form.DisplayForm):

    index = ViewPageTemplateFile('templates/tan_form.pt')

    def __call__(self):
        return self.index()

    def displayhtml(self):
        return displayhtml(PUBKEY, use_ssl=True)
