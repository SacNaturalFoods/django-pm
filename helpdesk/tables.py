"""
django-pm - A ticketing and project management tool.

(c) Copyright 2012 Sacramento Natural Foods Co-op, Inc. All Rights Reserved. See LICENSE for details.

tables.py - django-tables2 table classes 
"""

import django_tables2 as tables

class TicketTable(tables.Table):
    id = tables.Column()
    priority = tables.Column()
    title = tables.Column()
    queue = tables.Column()
    status = tables.Column()

    class Meta:
        attrs = {'class': 'paleblue'}
    
