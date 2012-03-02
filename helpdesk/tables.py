"""
django-pm - A ticketing and project management tool.

(c) Copyright 2012 Sacramento Natural Foods Co-op, Inc. All Rights Reserved. See LICENSE for details.

tables.py - django-tables2 table classes 
"""

import django_tables2 as tables
from django_tables2.utils import A

class TicketTable(tables.Table):
    id = tables.Column()
    priority = tables.Column()
    title = tables.LinkColumn('helpdesk_view', args=[A('id')])
    queue = tables.Column()
    status = tables.Column()
    
    #def render_title(self, value):
    #    return '<a href="%s">%s</a>' % (value.get_absolute_url, value.title)

    class Meta:
        attrs = {'class': 'paleblue'}
    
