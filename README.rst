django-pm - A Django powered project management tool and ticket system.
=======================================================================

Copyright 2012 Tony Schmidt and Sacramento Natural Foods Co-op, Inc.

Based on django-helpdesk by Ross Poulton.

Complete documentation is available in the docs/ directory, or #TODO: online at http://django-pm.readthedocs.org/.

Licensing
=========

Django-pm is a "mixed licensed" project.  Many files from the original django-helpdesk project are licensed under
a permissive license (LICENSE.django-helpdesk).  New files are licensed under the GNU Affero General Public 
License (see LICENSE).  Note that django-pm is also  distributed with 3rd party products which have their own 
licenses. See LICENSE.3RDPARTY for license terms for included packages.  It is the intention of the author that 
all future modifications and new files be subject to the AGPLv3.

Dependencies
============

Python 2.5+
git (to fetch the source for the django-haystack 2.0 beta)
libxslt1-dev (to support the python lxml and gdata libraries for Google Apps integration)

All other dependencies should be listed in `requirements.txt`.  As of this writing, they include the following:

Django==1.4 #to support native Selenium testing
django-tables2==0.9.4
South==0.7.3
-e git+https://github.com/toastdriven/django-haystack.git@4fb267623b58c5581be96a9a9504ca10a72eb0d8#egg=django_haystack-dev
django-taggit==0.9.3
gdata==2.0.15
httplib2==0.7.2
lxml==2.3
markup==0.2
pysolr==2.1.0-beta 

You will also need to set up a working Django project with a database, etc., before installing this app.

**NOTE REGARDING MySQL:**
If you use MySQL, with most default configurations you will receive an error 
when creating the database tables as we populate a number of default templates 
in languages other than English. 

You must create the database the holds the django-helpdesk tables using the 
UTF-8 collation; see the MySQL manual for more information: 
http://dev.mysql.com/doc/refman/5.1/en/charset-database.html

If you do NOT do this step, and you only want to use English-language templates,
you can continue however you will receive a warning when running the 'migrate'
commands.

Installation
============

#TODO: ``pip install django-pm``

For further installation information see docs/install.html and docs/configuration.html

Internationalisation
====================

If you want to help translate django-pm into languages other than English, we encourage you to make use of our Transifex project.

#TODO: http://www.transifex.net/projects/p/django-pm/resource/core/

Feel free to request access to contribute your translations.
