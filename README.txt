===========
2factorauth
===========

(Document the 2factorauth project here.)
This project has been initially created with Bluebream version 1.0

Installation
============

Run the following steps::

  $ python bootstrap.py
  $ bin/buildout

If you have an error during the buildout process, you probably miss some
dependencies (development libs, tools and headers).

Tests
=====

Run::

  $ bin/test


Debugging
=========

To start a python interpreter with the same environment as your project, run::

  $ bin/breampy

To start a python interpreter with the same environment as  your project and
with access to the ZODB database, run::

  $ bin/paster shell debug.ini # or deploy.ini

Here, you can access the root folder through the `root` variable, and a debugger
object through variable `debugger` or `app`. This object allows you to simulate
requests to the application and to access the ZODB root object.

Startup
=======

Check the WSGI configuration in deploy.ini and debug.ini

During development, run the following command to run the server::

  $ bin/paster serve debug.ini

For deployment, run::

  $ bin/paster serve --daemon deploy.ini

and use a process monitoring tool such as supervisord.


