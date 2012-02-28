"""
django-pm - A ticketing and project management tool.

(c) Copyright 2012 Sacramento Natural Foods Co-op, Inc. All Rights Reserved. See LICENSE for details.

views/search.py - autocomplete function for Haystack search. 
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
        [{'value': user.username, 'label': 'username', 'desc': user.username} for user in users]
        # + ["<b>ticket: </b>%s" % ticket.title for ticket in tickets] + 
        # + ["<b>queue: </b>%s" % queue.title for queue in queues]
        ))
    

