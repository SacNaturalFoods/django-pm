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

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.template import RequestContext

from haystack.views import SearchView
from django_tables2 import RequestConfig

from helpdesk.models import Ticket, Queue
from helpdesk.tables import TicketTable


class TabularSearchView(SearchView):
    def __name__(self):
        return "TabularSearchView"

    #def build_page(self):
    #    page = super(TabularSearchView, self).build_page()
    #    return None 

    #def get_results(self):
    #    results = super(TabularSearchView, self).get_results()

    #    table = TicketTable(results)

    #    return table 

    #def extra_context(self):
    #    extra = super(TabularSearchView, self).extra_context()

    #    table = TicketTable([{'id':result.object.pk, 'title':result.object.title} for result in self.results])
    #    RequestConfig(self.request).configure(table)
    #    extra['table'] = table 
    #    #extra['table'] = TicketTable([{'name':'foo', 'id':'bar'}, {'name':'baz', 'id':'gazi'}])

    #    return extra

    def create_response(self):
        table = TicketTable([{
            'id':result.object.pk, 
            'priority':result.object.priority,
            'title':result.object.title,
            'queue':result.object.queue,
            'status':result.object.status,
            } for result in self.results])
        RequestConfig(self.request).configure(table)
        context = {
            'query': self.query,
            'form': self.form,
            'table': table,
        }

        return render_to_response(self.template, context, context_instance=RequestContext(self.request))


def autocomplete_search(request):
    term = request.GET.get('term','')
    users = User.objects.filter(is_active=True, is_staff=True).filter(username__icontains=term).order_by('username')
    tickets = Ticket.objects.filter(title__icontains=term).order_by('title')
    queues = Queue.objects.filter(title__icontains=term).order_by('title')
    return HttpResponse(json.dumps(
        [{'label': 'username', 'value': user.username} for user in users]
        + [{'label': 'ticket', 'value': ticket.title} for ticket in tickets]
        + [{'label': 'queue', 'value': queue.title} for queue in queues]
        ))

