"""
django-pm - A ticketing and project management tool.

(c) Copyright 2012 Sacramento Natural Foods Co-op, Inc. All Rights Reserved. See LICENSE for details.

views/search.py - Autocomplete subclass for Haystack search. 
"""
from helpdesk.models import Ticket, Queue

from haystack.views import FacetedSearchView 
from haystack.query import SearchQuerySet 

from django.http import HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.models import User

class AutocompleteFacetedSearchView(FacetedSearchView):

    __name__ = 'AutocompleteFacetedSearchView'

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        if self.searchqueryset is None:
            #sqs = SearchQuerySet().filter(content_auto=self.request.GET.get('q', ''))
            sqs = SearchQuerySet().filter(owner_auto=self.request.GET.get('q','')).facet('queue').facet('assigned_to').facet('priority').facet('tags')
            import ipdb; ipdb.set_trace()   
            form_kwargs['searchqueryset'] = sqs

        return super(AutocompleteFacetedSearchView, self).build_form(form_kwargs)


def autocomplete_search(request):
    #term = request.GET.get('term','').split(' ')[-1]
    term = request.GET.get('term','')
    users = User.objects.filter(is_active=True, is_staff=True).filter(username__icontains=term).order_by('username')
    tickets = Ticket.objects.filter(title__icontains=term).order_by('title')
    queues = Queue.objects.filter(title__icontains=term).order_by('title')
    return HttpResponse(json.dumps(
        [user.username for user in users] + [ticket.title for ticket in tickets] + [queue.title for queue in queues]
        ))
    

