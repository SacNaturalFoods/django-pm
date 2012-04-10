"""
django-pm - A ticketing and project management tool.

(c) Copyright 2012 Sacramento Natural Foods Co-op, Inc. All Rights Reserved. See LICENSE for details.

tables.py - django-tables2 table classes 
"""

import django_tables2 as tables
from django_tables2.utils import A
from django_tables2 import Attrs

from helpdesk.models import Ticket 

class TicketTable(tables.Table):
    order_html = tables.Column(verbose_name='order', sortable=True, order_by=('order',))
    id = tables.Column(sortable=True)
    priority = tables.Column(sortable=True)
    title = tables.LinkColumn('helpdesk_view', args=[A('id')], sortable=True)
    assigned_to = tables.Column(verbose_name='owner', sortable=True)
    queue = tables.Column(sortable=True)
    status = tables.Column(sortable=True)
    created = tables.Column(sortable=True)

    def render_priority(self, value):
        return dict(Ticket.PRIORITY_CHOICES)[int(value)].split(' ')[-1]

    # can't get record values?
    #def render_order(self, value):
    #    return '<input id="ticket__%s" class="order" type="text" size="2" value="%s"/>' % (self.id, value)
    
    class Meta:
        attrs = {'class': 'paleblue'}
    
