"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

urls.py - Mapping of URL's to our various views. Note we always used NAMED
          views for simplicity in linking later on.
"""

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
# deprecated in Django 1.4
#from django.contrib.syndication.views import feed as django_feed

from helpdesk import settings as helpdesk_settings
#from helpdesk.views.feeds import feed_setup


urlpatterns = patterns('helpdesk.views.staff',
    url(r'^dashboard/$',
        'dashboard',
        name='helpdesk_dashboard'),

    url(r'^projects/(?P<project_id>[0-9]+)?',
        'view_projects',
        name='helpdesk_view_projects'),

    url(r'^project/(?P<project_id>[0-9]+)/$',
        'view_project',
        name='helpdesk_view_project'),

    url(r'^milestone/(?P<milestone_id>[0-9]+)/$',
        'edit_milestone',
        name='helpdesk_edit_milestone'),

    url(r'^delete_time_entry/(?P<time_entry_id>[0-9]+)/$',
        'delete_time_entry',
        name='helpdesk_delete_time_entry'),

    url(r'^edit_time_entry/(?P<time_entry_id>[0-9]+)?',
        'edit_time_entry',
        name='helpdesk_edit_time_entry'),

    url(r'^tickets/$',
        'ticket_list',
        name='helpdesk_list'),

    url(r'^tickets/update/$',
        'mass_update',
        name='helpdesk_mass_update'),

    url(r'^tickets/submit/$',
        'create_ticket',
        name='helpdesk_submit'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/$',
        'view_ticket',
        name='helpdesk_view'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/followup_edit/(?P<followup_id>[0-9]+)/$',
        'followup_edit',
        name='helpdesk_followup_edit'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/edit/$',
        'edit_ticket',
        name='helpdesk_edit'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/update/$',
        'update_ticket',
        name='helpdesk_update'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/delete/$',
        'delete_ticket',
        name='helpdesk_delete'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/hold/$',
        'hold_ticket',
        name='helpdesk_hold'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/unhold/$',
        'unhold_ticket',
        name='helpdesk_unhold'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/cc/$',
        'ticket_cc',
        name='helpdesk_ticket_cc'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/cc/add/$',
        'ticket_cc_add',
        name='helpdesk_ticket_cc_add'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/cc/delete/(?P<cc_id>[0-9]+)/$',
        'ticket_cc_del',
        name='helpdesk_ticket_cc_del'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/dependency/add/$',
        'ticket_dependency_add',
        name='helpdesk_ticket_dependency_add'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/dependency/delete/(?P<dependency_id>[0-9]+)/$',
        'ticket_dependency_del',
        name='helpdesk_ticket_dependency_del'),
        
    url(r'^tickets/(?P<ticket_id>[0-9]+)/attachment_delete/(?P<attachment_id>[0-9]+)/$',
        'attachment_del',
        name='helpdesk_attachment_del'),

    url(r'^tickets/(?P<ticket_id>[0-9]+)/attachment_download/(?P<attachment_id>[0-9]+)/$',
        'attachment_download',
        name='helpdesk_attachment_download'),

    url(r'^raw/(?P<type>\w+)/$',
        'raw_details',
        name='helpdesk_raw'),

    #url(r'^rss/$',
    #    'rss_list',
    #    name='helpdesk_rss_index'),

    url(r'^reports/$',
        'report_index',
        name='helpdesk_report_index'),

    url(r'^reports/(?P<report>\w+)/$',
        'run_report',
        name='helpdesk_run_report'),

    url(r'^save_query/$',
        'save_query',
        name='helpdesk_savequery'),

    url(r'^delete_query/(?P<id>[0-9]+)/$',
        'delete_saved_query',
        name='helpdesk_delete_query'),

    url(r'^settings/$',
        'user_settings',
        name='helpdesk_user_settings'),

    url(r'^ignore/$',
        'email_ignore',
        name='helpdesk_email_ignore'),

    url(r'^ignore/add/$',
        'email_ignore_add',
        name='helpdesk_email_ignore_add'),

    url(r'^ignore/delete/(?P<id>[0-9]+)/$',
        'email_ignore_del',
        name='helpdesk_email_ignore_del'),
)

urlpatterns += patterns('helpdesk.views.public',
    url(r'^$',
        'homepage',
        name='helpdesk_home'),

    url(r'^view/$',
        'view_ticket',
        name='helpdesk_public_view'),

    url(r'^change_language/$',
        'change_language',
        name='helpdesk_public_change_language'),        
)

urlpatterns += patterns('',
    # deprecated pattern in Django 1.4
    #url(r'^rss/(?P<url>.*)/$',
    #    login_required(django_feed),
    #    {'feed_dict': feed_setup},
    #    name='helpdesk_rss'),

    url(r'^api/(?P<method>[a-z_-]+)/$',
        'helpdesk.views.api.api',
        name='helpdesk_api'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'helpdesk/registration/login.html'},
        name='login'),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'helpdesk/registration/login.html', 'next_page': '../'},
        name='logout'),

    url(r'helpdesk/', include('social_auth.urls')),

    #url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    #url(r'^taggit_autocomplete/', include('taggit_autocomplete.urls')),
    url(r'^tagging_autocomplete_tagit/', include('tagging_autocomplete_tagit.urls')),
    
)

if helpdesk_settings.HELPDESK_KB_ENABLED:
    urlpatterns += patterns('helpdesk.views.kb',
        url(r'^kb/$',
            'index', name='helpdesk_kb_index'),
        
        url(r'^kb/(?P<item>[0-9]+)/$',
            'item', name='helpdesk_kb_item'),

        url(r'^kb/(?P<item>[0-9]+)/vote/$',
            'vote', name='helpdesk_kb_vote'),

        url(r'^kb/(?P<slug>[A-Za-z0-9_-]+)/$',
            'category', name='helpdesk_kb_category'),
    )

urlpatterns += patterns('',
    url(r'^api/$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'helpdesk/help_api.html',},
        name='helpdesk_api_help'),

    url(r'^help/context/$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'helpdesk/help_context.html',},
        name='helpdesk_help_context'),

    url(r'^system_settings/$',
        'django.views.generic.simple.direct_to_template',
        {
            'template': 'helpdesk/system_settings.html',
            'extra_context': {
                'ADMIN_URL': getattr(settings, 'ADMIN_URL', '/admin/'),
            },
        },
        name='helpdesk_system_settings'),
)


from haystack.query import SearchQuerySet
from haystack.forms import SearchForm
from helpdesk.forms import AllResultsSearchForm
from helpdesk.views.search import TabularSearchView
sqs = SearchQuerySet()

urlpatterns += patterns('helpdesk.views.search',
    url(r'^search/$', TabularSearchView(form_class=AllResultsSearchForm, searchqueryset=sqs, load_all=True), name='haystack_search'),
    url(r'^search/autocomplete/$','autocomplete_search', name='autocomplete_search'),
    url(r'^search/save$','save_search', name='save_search'),
    url(r'^search/delete$','delete_search', name='delete_search'),
    url(r'^search/toggle_sticky$','toggle_sticky_search', name='toggle_sticky'),
    url(r'^search/change_ticket_order$','change_ticket_order', name='change_ticket_order'),
    )

urlpatterns += patterns('',
        url(r'^chaining/', include('smart_selects.urls')),
        )


