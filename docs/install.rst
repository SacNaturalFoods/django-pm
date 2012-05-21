Installation
============

django-pm installation isn't difficult, but it requires you have a bit of existing know-how about Django.


Getting The Code
----------------

Installing using PIP
~~~~~~~~~~~~~~~~~~~~

Try using #TODO: ``pip install django-pm``. Go and have a beer to celebrate Python packaging.

GIT Checkout (Cutting Edge)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're planning on editing the code or just want to get whatever is the latest and greatest, you can 
clone the official Git repository with ``git clone git://github.com/SacNaturalFoods/django-pm.git``

Copy the ``helpdesk`` folder into your ``PYTHONPATH``.

I just want a .tar.gz!
~~~~~~~~~~~~~~~~~~~~~~

#TODO: You can download the latest PyPi package from http://pypi.python.org/pypi/django-pm/

Download, extract, and drop ``helpdesk`` into your ``PYTHONPATH``

Adding To Your Django Project
-----------------------------

#. Edit your ``settings.py`` file and add ``helpdesk`` to the ``INSTALLED_APPS`` setting. You also need ``django.contrib.admin`` and ``taggit``.  The rest of the dependencies are managed in django-pm's ``settings.py``::
    
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin', # Required for helpdesk admin/maintenance
        'taggit', # required for tagging
        'helpdesk',
    )

    # for search
    import os
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        },
    }

    # your django-pm settings (example)
    HELPDESK_CALENDAR = 'google'
    HELPDESK_UPDATE_CALENDAR = False 

    QUEUE_EMAIL_BOX_TYPE = 'imap'
    QUEUE_EMAIL_BOX_SSL = True 
    QUEUE_EMAIL_BOX_HOST = 'imap.gmail.com'
    QUEUE_EMAIL_BOX_USER = 'yourqueueemail@yourdomain.com'
    QUEUE_EMAIL_BOX_PASSWORD = 'yourqueueemailpassword'

    # Social auth settings (example)
    SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
    GOOGLE_CONSUMER_KEY = 'yourconsumerkey'
    GOOGLE_CONSUMER_SECRET = 'yourconsumersecret'
    GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.google.com/calendar/feeds/']
    GOOGLE_WHITE_LISTED_DOMAINS = ['yourdomain.com']
    GOOGLE_WHITE_LISTED_EMAILS = ['someoutsideemail@gmail.com']

#. If you haven't installed django-pm with ``pip``, then you will need to explicitly install the dependencies::

     pip install -r requirements.txt 

    As well as put django-pm on your python path::
     
     python setup.py develop

#. Make sure django-pm is accessible via ``urls.py``. Add the following line to ``urls.py``::

     (r'helpdesk/', include('helpdesk.urls')),

   Note that you can change 'helpdesk/' to anything you like, such as 'support/' or 'help/'. If you want django-helpdesk to be available at the root of your site (for example at http://support.mysite.tld/) then the line will be as follows::
     
     (r'', include('helpdesk.urls')),

   This line will have to come *after* any other lines in your urls.py such as those used by the Django admin.
   
   You will also need to add the django_socialauth urls for oauth2 login::

     (r'login/$', 'social_auth.views.auth', {'backend': 'google-oauth2'}),

#. Create the required database tables. I'd suggest using *South*, however the following will work::

     ./manage.py syncdb

   Then migrate using South::

     ./manage.py migrate helpdesk

#. Make sure your webserver can write to your upload directory, e.g::

      chown www-data:www-data [your MEDIA_ROOT] 
      chmod 700 [your MEDIA_ROOT] 

   (substitute www-data for the user / group that your web server runs as, eg 'apache' or 'httpd')

#. Ensure that your ``MEDIA_ROOT`` folder has directory listings turned off, to ensure users don't download files that they are not specifically linked to from their tickets.

   If you are using Apache, put a ``.htaccess`` file in the ``MEDIA_ROOT`` folder with the following content::

      Options -Indexes

   You will also have to make sure that ``.htaccess`` files aren't being ignored.


Configuring Apache with mod_wsgi
--------------------------------

#. Add your python environment site-packages, project configuration (or project parent directory) and project root paths to ``myproject/wsgi.py``, e.g.::

    import site
    site.addsitedir('/opt/myproject/lib/python2.6/site-packages')
    import os
    import sys
    sys.path.append('/opt/myproject/conf')
    sys.path.append('/opt/myproject/conf/myproject')

#. Configure the Apache virtual host for your site::

    <VirtualHost *:80>
            ServerName mysite.com

            WSGIScriptAlias / /opt/myproject/conf/myproject/wsgi.py

            # serve static files
            Alias /media/ /opt/myproject/data/sitestatic/media/
            Alias /js/ /opt/myproject/data/sitestatic/js/
            Alias /static/ /opt/myproject/data/sitestatic/

            <Directory /opt/myproject/data/sitestatic>
                    Order deny,allow
                    Allow from all
            </Directory>
    </VirtualHost>
