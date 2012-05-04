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

1. Edit your ``settings.py`` file and add ``helpdesk`` to the ``INSTALLED_APPS`` setting. You also need ``django.contrib.admin`` in ``INSTALLED_APPS`` if you haven't already added it. eg::
    
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin', # Required for helpdesk admin/maintenance
        'django.contrib.markup', # Required for text display
        'south', 
        'taggit',
        'taggit_autosuggest',
        'django_tables2',
        'social_auth',
        'haystack', # for search
        'helpdesk', # This is new!
    )

    # for django_tables2
    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.contrib.messages.context_processors.messages",
        "django.core.context_processors.request",
    )

    # for social_auth
    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.google.GoogleOAuthBackend',
        'django.contrib.auth.backends.ModelBackend',
        )

    # for search
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'http://127.0.0.1:8983/solr'
        },
    }

    # your django-pm settings (example)
    HELPDESK_ALLOW_NON_STAFF_TICKET_UPDATE = True 
    HELPDESK_NAVIGATION_ENABLED = True 
    HELPDESK_CUSTOM_WELCOME = True 
    HELPDESK_VIEW_A_TICKET_PUBLIC = False 
    HELPDESK_SUBMIT_A_TICKET_PUBLIC = False 
    HELPDESK_KB_ENABLED_STAFF = True
    HELPDESK_STAFF_ONLY_TICKET_OWNERS = True
    HELPDESK_STAFF_ONLY_TICKET_CC = True
    HELPDESK_CALENDAR = 'google'
    HELPDESK_UPDATE_CALENDAR = False 
    HELPDESK_FOLLOWUP_MOD = True
    HELPDESK_INCLUDE_DESCRIPTION_IN_FOLLOWUP = False

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

2. Make sure django-pm is accessible via ``urls.py``. Add the following line to ``urls.py``::

     (r'helpdesk/', include('helpdesk.urls')),

   Note that you can change 'helpdesk/' to anything you like, such as 'support/' or 'help/'. If you want django-helpdesk to be available at the root of your site (for example at http://support.mysite.tld/) then the line will be as follows::
     
     (r'', include('helpdesk.urls')),

   This line will have to come *after* any other lines in your urls.py such as those used by the Django admin.

3. Create the required database tables. I'd suggest using *South*, however the following will work::

     ./manage.py syncdb

   Then migrate using South

     ./manage.py migrate helpdesk

4. [If you're not using django.contrib.staticfiles] Inside your ``STATIC_ROOT`` folder, create a new folder called ``helpdesk`` and copy the contents of ``helpdesk/static`` into it. Alternatively, create a symlink::

      ln -s /path/to/helpdesk/static/helpdesk /path/to/static/helpdesk

5. Inside your ``MEDIA_ROOT`` folder, inside the ``helpdesk`` folder, is a folder called ``attachments``. Ensure your web server software can write to this folder - something like this should do the trick::

      chown www-data:www-data attachments/
      chmod 700 attachments

   (substitute www-data for the user / group that your web server runs as, eg 'apache' or 'httpd')

   If all else fails ensure all users can write to it::

      chmod 777 attachments/

   This is NOT recommended, especially if you're on a shared server.

6. Ensure that your ``attachments`` folder has directory listings turned off, to ensure users don't download files that they are not specifically linked to from their tickets.

   If you are using Apache, put a ``.htaccess`` file in the ``attachments`` folder with the following content::

      Options -Indexes

   You will also have to make sure that ``.htaccess`` files aren't being ignored.

   Ideally, accessing http://MEDIA_URL/helpdesk/attachments/ will give you a 403 access denied error.

7. If it's not already installed, install ``python-markdown``::

      pip install Markdown

8. If you already have a view handling your logins, then great! If not, add the following to ``settings.py`` to get your Django installation to use the login view included in ``django-helpdesk``::

      LOGIN_URL = '/helpdesk/login/'

   Alter the URL to suit your installation path.


Configuring Solr
----------------

django-pm uses django-haystack + Apache Solr for faster searching.

Configuring Apache with mod_wsgi
--------------------------------
