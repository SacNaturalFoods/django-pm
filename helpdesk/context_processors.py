"""
django-pm - A ticketing and project management tool.

Copyright (C) 2012 Sacramento Natural Foods Co-op, Inc. and Tony Schmidt

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

from helpdesk.models import SavedSearch

def saved_searches(request):
    if request.user.is_authenticated():
        return {'saved_searches': ' '.join([search.html for search in SavedSearch.objects.filter(user=request.user).all()])}
    return {}


