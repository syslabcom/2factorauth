import hashlib
import logging
# import netifaces
import random
from datetime import datetime
from datetime import timedelta
from email.MIMEText import MIMEText
# from loops.util import _
from recaptcha.client.captcha import submit
from zope import component
from zope.app.authentication.session import SessionCredentialsPlugin
from zope.interface import implements
from zope.publisher.interfaces.http import IHTTPRequest
from zope.sendmail.interfaces import IMailDelivery
from zope.session.interfaces import ISession
from zope.pluggableauth.plugins.session import ISessionCredentials
from zope.pluggableauth.plugins.session import SessionCredentials

TIMEOUT = timedelta(minutes=5)
PRIVKEY = "6LcGPQ4TAAAAABCyA_BCAKPkD6wW--IhUicbAZ11"
log = logging.getLogger('2FactorAuth')


class ITwoFactorSessionCredentials(ISessionCredentials):
    """Interface for storing and accessing credentials in a session.

    We use a real class with interface here to prevent unauthorized
    access to the credentials.
    """

    def __init__(login, password):  # noqa
        pass

    # def getLogin():  # noqa
    #     """Return login name."""

    # def getPassword():  # noqa
    #     """Return password."""

    def getTAN():  # noqa
        """Return a random TAN"""

    def getTimestamp():  # noqa
        """Return the timestamp of the request"""


class TwoFactorSessionCredentials(SessionCredentials):
    """Credentials class for use with sessions.

    A session credential is created with a login and a password:

      >>> cred = SessionCredentials('scott', 'tiger')

    Logins are read using getLogin:
      >>> cred.getLogin()
      'scott'

    and passwords with getPassword:

      >>> cred.getPassword()
      'tiger'

    """
    implements(ITwoFactorSessionCredentials)

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.tan = random.randint(10000000, 99999999)
        self.timestamp = datetime.now()
        rng = range(8)
        self.tanA = random.choice(rng)
        rng.remove(self.tanA)
        self.tanB = random.choice(rng)
        self.hash = hashlib \
            .sha224("%s:%s:%s" % (login, password, self.tan)) \
            .hexdigest()
        self.validated = False


class TwoFactorSessionCredentialsPlugin(SessionCredentialsPlugin):

    tan_a_field = 'tan_a'
    tan_b_field = 'tan_b'
    hash_field = 'hash'


    def extractCredentials(self, request):  # noqa
        """Extracts credentials from a session if they exist."""
        if not IHTTPRequest.providedBy(request):
            return None
        session = ISession(request)
        # Fun. Direct access created a default. .get doesn't
        session_data = session['zope.pluggableauth.browserplugins']
        login = request.get(self.loginfield, None)
        password = request.get(self.passwordfield, None)
        tan_a = request.get(self.tan_a_field, None)
        tan_b = request.get(self.tan_b_field, None)
        hash = request.get(self.hash_field, None)
        credentials = None
        redirect = request.response.redirect

        def _validate_tans(a, b, creds):
            tan = str(creds.tan)
            if tan[creds.tanA] == a and \
               tan[creds.tanB] == b:
                return True
            return False

        def _validate_captcha():
            return submit(request['recaptcha_challenge_field'],
                          request['recaptcha_response_field'],
                          PRIVKEY,
                          '')
            # netifaces.ifaddresses('eth0')[2][0]['addr']
        if login and password and not tan_a and not tan_b and not hash:
            # 1st phase, user has provided login and password
            log.info('First Phase: Got login and password, no TANs.')

            credentials = TwoFactorSessionCredentials(login, password)
            session_data['credentials'] = credentials
            # Send email to user
            self.send_tan_email(login, credentials.tan)
            log.info("Thank you for logging in. Then Tan is %s. " %
                     credentials.tan)
            url = '%s/@@tanForm.html?h=%s&a=%s&b=%s' % \
                  (request.getURL(),
                   credentials.hash,
                   credentials.tanA + 1,
                   credentials.tanB + 1)
            if request.get('camefrom'):
                url += "&camefrom=%s" % request['camefrom']
            redirect(url)

        elif not login and not password and hash:
            # 2nd phase, user has given TANs and the hash.
            log.info('2nd Phase. No login or password, but TANs.')
            credentials = session_data.get('credentials', None)

            if not (tan_a and tan_b):
                msg = u"There was a problem reading your TAN digits. " + \
                      u"Please try again."
                log.info(msg)
                return redirect('@@tanForm.html?e=%s&hash=%s&a=%s&b=%s' %
                                (msg,
                                 hash,
                                 credentials.tanA + 1,
                                 credentials.tanB + 1))

            # Validate the captcha
            r = _validate_captcha()
            if not r.is_valid:
                msg = u"The captcha did not validate. Please try again."
                log.info(msg)
                return redirect(
                    '@@tanForm.html?e=%s&h=%s&a=%s&b=%s&tan_a=%s&tan_b=%s' %
                    (msg,
                     hash,
                     credentials.tanA + 1,
                     credentials.tanB + 1,
                     tan_a,
                     tan_b))

            log.info('The captcha is valid, continuing...')

            # No credentials, fail
            if not credentials:
                msg = u"We couldn't find your credentials. Please try again."
                log.info(msg)
                return redirect('@@loginForm.html?e=%s' %
                                (msg))

            # No or wrong hash provided, fail
            if credentials.hash != hash:
                msg = u"Somehow this page doesn't fit to the previous one." + \
                      u"Please start from scratch."
                log.info(msg)
                return redirect('@@loginForm.html?e=%s' %
                                (msg))

            # Took longer than TIMEOUT, fail
            if credentials.timestamp < datetime.now() - TIMEOUT:
                msg = u"A timeout has been reached. " + \
                      u"Please start from scratch."
                log.info(msg)
                return redirect('@@loginForm.html?e=%s' %
                                (msg))

            # Can't validate tans, fail
            if not _validate_tans(tan_a, tan_b, credentials):
                msg = u"The provided TAN digits don't fit. Please try again."
                log.info(msg)
                return redirect('@@tanForm.html?e=%s&a=%s&b=%s' %
                                (msg,
                                 credentials.tanA + 1,
                                 credentials.tanB + 1))

            credentials.validated = True
            log.info('Credentials are valid')

            session_data['credentials'] = credentials
            if request.get('camefrom'):
                redirect(request.get('camefrom'))
            else:
                redirect('./@@contents.html')
        elif not session_data:
            # Just display loginForm.html
            return None

        session_data = session['zope.pluggableauth.browserplugins']
        credentials = session_data.get('credentials', None)

        if not credentials:
            log.info('credentials are None')
            return None

        if not credentials.validated:
            log.warn("User is not validated. Don't log in!")
            return None

        log.info("All fine, user can be logged in, return credentials.")
        return {'login': credentials.getLogin(),
                'password': credentials.getPassword()}

    def challenge(self, request):
        request.response.redirect('%s/@@%s' %
                                  (request.URL.get(-1), self.loginpagename))
        return True

    def send_tan_email(self, userid, tan):
        # XXX: Resolve email from userid
        recipient = u'pilz@syslab.com'

        recipients = [recipient]
        # Needs Loops integration for translations
        # subject = _(u'tan_mail_subject')
        # message = _(u'tan_mail_text') + u':\n\n'
        subject = u'Your log in TAN'
        message = u'Dear User,\n\nyou just attempted to log into our web site. ' + \
                  u'To continue you need to enter two digits of the attached ' + \
                  u'number:\n\n%s\n\nWhich digits to enter is stated on the login ' + \
                  u'page.\n\n\nThank you!'

        message = (message % tan).encode('UTF-8')

        # Needs Loops integration for Options
        # sender_info = self.globalOptions('email.sender')
        sender_info = None
        sender = sender_info and sender_info[0] or 'info@loops.cy55.de'
        sender = sender.encode('UTF-8')
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = subject.encode('UTF-8')
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        mailhost = component.getUtility(IMailDelivery, 'Mail')
        mailhost.send(sender, recipients, msg.as_string())
