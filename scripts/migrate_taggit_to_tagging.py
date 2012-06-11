#!/opt/snfc/projects/bin/python

import os, sys
sys.path.append(os.path.abspath('/opt/snfc/projects/conf'))

from django.core.management import setup_environ
from projects import settings
setup_environ(settings)

from taggit.models import TaggedItem

for tagged_item in TaggedItem.objects.all():
    tagged_item.content_object.tags += " %s" % tagged_item.tag.name
    print tagged_item.tag.name
    print tagged_item.content_object
    print tagged_item.content_object.tags
    tagged_item.content_object.save()
