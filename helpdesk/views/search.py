"""
django-pm - A ticketing and project management tool.

Copyright (C) 2012 Sacramento Natural Foods Co-op, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from urllib import urlencode
from urlparse import urlparse, parse_qs
import re

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.template import RequestContext

from haystack.views import SearchView
from haystack.query import SearchQuerySet
from django_tables2 import RequestConfig
from taggit.models import Tag

from helpdesk.models import Ticket, Queue, SavedSearch
from helpdesk.tables import TicketTable


class TabularSearchView(SearchView):

    def __name__(self):
        return "TabularSearchView"

    # funky request action - iframes keep parent request in templates, screws up pagination and sorting
    # need to pass new requests to response if iframes, but not main page
    def __call__(self, request):
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response(request)

    # TODO: refactor, explain iframe/request wierdness
    def create_response(self, request):
        table = TicketTable([{
            'order':result.object.order,
            'order_html':result.object.order_html(),
            'id':result.object.pk, 
            'priority':result.object.priority,
            'title':result.object.title if len(result.object.title) < 51 else result.object.title[:50]+'...',
            'assigned_to':result.object.assigned_to.username if result.object.assigned_to else None,
            'queue':result.object.queue,
            'status':result.object.status_str,
            'created':result.object.created.strftime('%Y-%m-%d'),
            } for result in self.results])
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        sticky = request.GET.get('sticky', None)
        # iframes
        if sticky is not None:
            sticky = True if sticky == 'true' else False
            template = 'helpdesk/table.html'
            q = request.GET.copy()
            del q['sticky']
            existing_saved_search = SavedSearch.objects.filter(
                    query=q.urlencode(), user=self.request.user).exists()
            context = {'table': table, 'sticky':sticky, 'existing_saved_search': existing_saved_search}
            return render_to_response(template, context, context_instance=RequestContext(request))
        # main page
        else:
            query = self.request.META['QUERY_STRING']
            template = self.template
            sticky_searches = [s for s in SavedSearch.objects.filter(user=self.request.user, sticky=True).all()]
            if query:
                sticky_searches = [SavedSearch(query=query)] + sticky_searches
            context = {
                'query': query,
                'form': self.form,
                'table': table,
                'existing_saved_search': SavedSearch.objects.filter(
                    query=self.request.META.get('QUERY_STRING'), user=self.request.user).exists(),
                'saved_searches': ' '.join([
                    search.html for search in SavedSearch.objects.filter(user=self.request.user).all()]),
                'sticky_searches': sticky_searches,
            }
            return render_to_response(template, context, context_instance=RequestContext(self.request))



def autocomplete_search(request):
    term = request.GET.get('term','')
    users = User.objects.filter(is_active=True, is_staff=True).filter(username__icontains=term).order_by('username')
    priorities = []
    for priority in ['critical', 'high', 'normal', 'low', 'very low']:
        if term.lower() in priority:
            priorities.append(priority.capitalize())
    statuses = []
    for status in ['open', 'resolved', 'closed']:
        if term.lower() in status:
            statuses.append(status.capitalize())
    tags = Tag.objects.filter(name__icontains=term)
    tickets = Ticket.objects.filter(title__icontains=term).order_by('title')
    queues = Queue.objects.filter(title__icontains=term).order_by('title')
    return HttpResponse(json.dumps(
        [{'label': 'list', 'value': queue.title} for queue in queues]
        + [{'label': 'assigned_to', 'value': user.username} for user in users]
        + [{'label': 'submitted_by', 'value': user.username} for user in users]
        + [{'label': 'priority_str', 'value': priority} for priority in priorities]
        + [{'label': 'status_str', 'value': status} for status in statuses]
        + [{'label': 'tags', 'value': tag.name} for tag in tags]
        + [{'label': 'title', 'value': ticket.title} for ticket in tickets]
        ))

def save_search(request):
    q = parse_qs(urlparse(request.POST.get('href')).query)
    if q.has_key('sticky'):
        del q['sticky']
    saved_search, created = SavedSearch.objects.get_or_create(
            user=request.user, 
            query=urlencode(q, True),
            )
    saved_search.sticky = True if request.POST.get('sticky') == 'true' else False
    if request.POST.get('title') != 'null':
        saved_search.title = request.POST.get('title')
    saved_search.save()
    # TODO: hide this in model?
    saved_search.reorder()
    saved_searches = [search.html for search in SavedSearch.objects.filter(user=request.user).all()]
    return HttpResponse(saved_searches)

def delete_search(request):
    SavedSearch.objects.get(pk=request.POST.get('saved_search__pk')).delete()
    # use manager to return html property?
    saved_searches = [search.html for search in SavedSearch.objects.filter(user=request.user).all()]
    return HttpResponse(saved_searches)
    
def toggle_sticky_search(request):
    href = urlparse(request.POST.get('href')).query
    try:
        if href:
            try:
                saved_search = SavedSearch.objects.filter(user=request.user, query=urlencode(parse_qs(href), True))[0]
            except:
                saved_search = None
        if saved_search:
            saved_search.sticky = not saved_search.sticky
            saved_search.reorder()
            saved_search.order = 1
            saved_search.save()
    except Exception, e:
        print e
    return HttpResponse(status=200)
     
def change_ticket_order(request):
    ticket_id = request.POST.get('ticket_id')
    new_order = request.POST.get('new_order')
    Ticket.objects.get(pk=int(ticket_id)).reorder(int(new_order))
    return HttpResponse(status=200)



