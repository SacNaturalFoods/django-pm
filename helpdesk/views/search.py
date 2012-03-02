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

from helpdesk.models import Ticket, Queue

from django.http import HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.models import User


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
    

