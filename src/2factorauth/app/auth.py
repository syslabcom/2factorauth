from zope.app.authentication.session import SessionCredentialsPlugin


class TwoFactorSessionCredentialsPlugin(SessionCredentialsPlugin):

    def challenge(self, request):

        request.response.redirect('@@' + self.loginpagename)
        return True
