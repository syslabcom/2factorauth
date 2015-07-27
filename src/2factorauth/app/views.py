from zope.container.interfaces import INameChooser
from zope.formlib import form

from interfaces import ITwoFactorApplication
from app import TwoFactorApplication

from zope.site import LocalSiteManager
from zope.pluggableauth.authentication import PluggableAuthentication
from zope.authentication.interfaces import IAuthentication
from zope.app.authentication.principalfolder import PrincipalFolder
# from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from zope.securitypolicy.interfaces import IPrincipalRoleManager
# from zope.securitypolicy.interfaces import IPrincipalPermissionManager
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility
from zope.principalannotation.utility import PrincipalAnnotationUtility
from zope.session.interfaces import ISessionDataContainer
from zope.session.session import PersistentSessionDataContainer

from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent, ObjectModifiedEvent
from zope.session.http import CookieClientIdManager
from zope.session.http import ICookieClientIdManager
from zope.app.authentication.principalfolder import InternalPrincipal


class AddTwoFactorApplication(form.AddForm):

    form_fields = form.Fields(ITwoFactorApplication)

    def setup_site_manager(self, context):
        context.setSiteManager(LocalSiteManager(context))
        sm = context.getSiteManager()
        pau = PluggableAuthentication(prefix='2f.pau.')
        notify(ObjectCreatedEvent(pau))
        sm[u'authentication'] = pau
        sm.registerUtility(pau, IAuthentication)

        annotation_utility = PrincipalAnnotationUtility()
        sm.registerUtility(annotation_utility, IPrincipalAnnotationUtility)
        session_data = PersistentSessionDataContainer()
        sm.registerUtility(session_data, ISessionDataContainer)

        client_id_manager = CookieClientIdManager()
        notify(ObjectCreatedEvent(client_id_manager))
        sm[u'CookieClientIdManager'] = client_id_manager
        sm.registerUtility(client_id_manager, ICookieClientIdManager)

        principals = PrincipalFolder(prefix='pf.')
        notify(ObjectCreatedEvent(principals))
        pau[u'pf'] = principals
        pau.authenticatorPlugins += (u"pf", )
        notify(ObjectModifiedEvent(pau))
        pau.credentialsPlugins = (u'TwoFactor Session Credentials',)

        p1 = InternalPrincipal('admin1', 'admin1', "Admin 1",
                               passwordManagerName="Plain Text")
        principals['p1'] = p1

        role_manager = IPrincipalRoleManager(context)
        login_name = principals.getIdByLogin(p1.login)
        pid = unicode('2f.pau.' + login_name)
        role_manager.assignRoleToPrincipal('zope.Manager', pid)

    def createAndAdd(self, data):  # noqa
        name = data['name']
        description = data.get('description')
        namechooser = INameChooser(self.context)
        app = TwoFactorApplication()
        name = namechooser.chooseName(name, app)
        app.name = name
        app.description = description
        self.setup_site_manager(app)
        self.context[name] = app
        self.request.response.redirect(name)


class TwoFactorApplicationDefaultView(form.DisplayForm):

    def __call__(self):
        return """Welcome to the TwoFactor application"""
