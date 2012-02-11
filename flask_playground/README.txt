== About ==

This fabricated example models bank transfers.

Web browser (User)   ->   App server (Flask)

Server:
    Flask
    SQLite - application state
    MySQL - GlobalBank
    PostgreSQL - PiggyBank 

Web browser:
    Requests -> server (template html)
    AJAX -> server (REST API)

== Installation ==

=== Prerequisites ===

* Python 2.7 with setuptools (easy_install) and virtualenv.
** http://pypi.python.org/pypi/setuptools#downloads
  easy_install virtualenv

* bash to run setup scripts. 
** On Windows, install cygwin and ensure it's on the path: http://www.cygwin.com/

=== Setup ===

Setup script (run once to create a virtualenv and pip install):
  bash flaskbanking/tools/setup/env_setup.sh

Optionally you can:
  pip install ipython

