from setuptools import setup, find_packages


setup(name='2factorauth',
      version='0.1',
      description='a 2 factor auth plugin',
      long_description="""\
""",
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords='',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='http://syslab.com',
      license='GPL2.0',
      package_dir={'': 'src'},
      packages=find_packages('src'),

      include_package_data=True,
      zip_safe=False,
      install_requires=['netifaces',
                        'recaptcha-client',
                        'setuptools',
                        'zope.securitypolicy',
                        'zope.component',
                        'zope.annotation',
                        'zope.browserresource',
                        'zope.app.dependable',
                        'zope.app.appsetup',
                        'zope.app.content',
                        'zope.publisher',
                        'zope.app.broken',
                        'zope.app.component',
                        'zope.app.generations',
                        'zope.app.error',
                        'zope.app.publisher',
                        'zope.app.security',
                        'zope.app.form',
                        'zope.app.i18n',
                        'zope.app.locales',
                        'zope.app.zopeappgenerations',
                        'zope.app.principalannotation',
                        'zope.app.basicskin',
                        'zope.app.rotterdam',
                        'zope.app.folder',
                        'zope.app.wsgi',
                        'zope.formlib',
                        'zope.i18n',
                        'zope.app.pagetemplate',
                        'zope.app.schema',
                        'zope.app.container',
                        'zope.app.debug',
                        'z3c.testsetup',
                        'zope.app.testing',
                        'zope.testbrowser',
                        'zope.login',
                        'zope.keyreference',
                        'zope.intid',
                        'zope.contentprovider',
                        'zope.app.zcmlfiles',
                        'zope.session',
                        'zope.sendmail'
                        ],
      entry_points="""
      [paste.app_factory]
      main = 2factorauth.startup:application_factory

      [paste.global_paster_command]
      shell = 2factorauth.debug:Shell
      """,
      )
