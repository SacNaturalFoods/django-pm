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

from urlparse import urlparse
from urlparse import parse_qs
import re

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.template import RequestContext

from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from django_tables2 import RequestConfig
from taggit.models import Tag

from helpdesk.models import Ticket, Queue, SavedSearch
from helpdesk.tables import TicketTable


class TabularSearchView(FacetedSearchView):
    def __name__(self):
        return "TabularSearchView"

    def create_response(self):
        table = TicketTable([{
            'id':result.object.pk, 
            'priority':result.object.priority_str,
            'title':result.object.title if len(result.object.title) < 31 else result.object.title[:30]+'...',
            'description':result.object.description if len(result.object.description) < 31 else result.object.description[:30]+'...',
            'assigned_to':result.object.assigned_to.username if result.object.assigned_to else None,
            'queue':result.object.queue,
            'status':result.object.status_str,
            'created':result.object.created.strftime('%Y-%m-%d'),
            } for result in self.results])
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        if self.request.GET.get('sticky',''):
            template = 'helpdesk/table.html'
            context = {'table': table, 'sticky':True}
        else:
            template = self.template
            context = {
                'query': self.query,
                'form': self.form,
                'table': table,
                'existing_saved_search': SavedSearch.objects.filter(
                    query=self.request.META.get('QUERY_STRING'), user=self.request.user).exists(),
                'saved_searches': ' '.join([
                    search.html for search in SavedSearch.objects.filter(user=self.request.user).all()]),
                'sticky_searches': SavedSearch.objects.filter(user=self.request.user, sticky=True).all(),
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
        [{'label': 'queue', 'value': queue.title} for queue in queues]
        + [{'label': 'assigned_to', 'value': user.username} for user in users]
        + [{'label': 'submitted_by', 'value': user.username} for user in users]
        + [{'label': 'priority_str', 'value': priority} for priority in priorities]
        + [{'label': 'status_str', 'value': status} for status in statuses]
        + [{'label': 'tags', 'value': tag.name} for tag in tags]
        + [{'label': 'title', 'value': ticket.title} for ticket in tickets]
        ))

def save_search(request):
    saved_search, created = SavedSearch.objects.get_or_create(
            user=request.user, 
            query=urlparse(request.POST.get('href')).query,
            )
    saved_search.sticky=request.POST.get('sticky') 
    if created:
        saved_search.title=request.POST.get('title')
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
    href = request.POST.get('href')
    try:
        if href:
            try:
                saved_search = SavedSearch.objects.filter(user=request.user, query=urlparse(href).query)[0]
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
     

