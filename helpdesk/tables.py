"""
django-pm - A ticketing and project management tool.

(c) Copyright 2012 Sacramento Natural Foods Co-op, Inc. All Rights Reserved. See LICENSE for details.

tables.py - django-tables2 table classes 
"""

import django_tables2 as tables
from django_tables2.utils import A
from django_tables2 import Attrs

class TicketTable(tables.Table):
    id = tables.Column(sortable=True)
    priority = tables.Column(sortable=True)
    title = tables.LinkColumn('helpdesk_view', args=[A('id')], sortable=True)
    assigned_to = tables.Column(verbose_name='owner', sortable=True)
    queue = tables.Column(sortable=True)
    status = tables.Column(sortable=True)
    created = tables.Column(sortable=True)
    
    class Meta:
        attrs = {'class': 'paleblue'}
    
