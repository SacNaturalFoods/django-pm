"""
django-pm - A ticketing and project management tool.

(c) Copyright 2012 Sacramento Natural Foods Co-op, Inc. All Rights Reserved. See LICENSE for details.

tables.py - django-tables2 table classes 
"""

import django_tables2 as tables
from django_tables2.utils import A
from django_tables2 import Attrs

from helpdesk.models import Ticket, Milestone

class TicketTable(tables.Table):
    order_html = tables.Column(verbose_name='order', sortable=True, order_by=('order',))
    id = tables.Column(sortable=True)
    priority = tables.Column(sortable=True)
    title = tables.LinkColumn('helpdesk_view', args=[A('id')], sortable=True)
    assigned_to = tables.Column(verbose_name='owner', sortable=True)
    list = tables.Column(sortable=True, verbose_name='list')
    milestone = tables.Column(sortable=True)
    status = tables.Column(sortable=True)
    due_date = tables.Column(sortable=True)
    modified = tables.Column(sortable=True)

    def render_priority(self, value):
        if value:
            return dict(Ticket.PRIORITY_CHOICES)[int(value)].split(' ')[-1]

    # can't get record values?
    #def render_order(self, value):
    #    return '<input id="ticket__%s" class="order" type="text" size="2" value="%s"/>' % (self.id, value)
    
    class Meta:
        attrs = {'class': 'paleblue'}


class MilestoneTicketTable(tables.Table):
    title = tables.LinkColumn('helpdesk_view', args=[A('id')], sortable=True)
    estimate = tables.Column(sortable=True)
    percent_complete = tables.Column(sortable=True)
    due_on = tables.Column(sortable=True)

    class Meta:
        attrs = {'class': 'paleblue'}


class TimeEntryTable(tables.Table):
    description = tables.Column()
    date_start = tables.Column()
    date_end = tables.Column()
    time = tables.Column()

    class Meta:
        orderable = False
        attrs = {'class': 'paleblue'}


class MilestoneTable(tables.Table):
    name = tables.LinkColumn('helpdesk_edit_milestone', args=[A('id')], sortable=True)
    due_on = tables.Column(sortable=True)
    estimate = tables.Column(sortable=True)
    percent_complete = tables.Column(sortable=True)
    total_tickets = tables.Column(sortable=True)
    closed_tickets = tables.Column(sortable=True)

    class Meta:
        attrs = {'class': 'paleblue'}
 
