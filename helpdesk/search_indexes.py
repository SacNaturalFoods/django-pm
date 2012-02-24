import datetime
from haystack import indexes
from helpdesk.models import Ticket


class TicketIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    owner = indexes.CharField(model_attr='assigned_to', null=True)
    #owner_auto = indexes.EdgeNgramField(model_attr='assigned_to', null=True)
    priority = indexes.CharField(model_attr='priority')
    project = indexes.CharField(model_attr='queue')
    #assigned_to = indexes.CharField(model_attr='assigned_to', faceted=True, null=True)
    #queue = indexes.CharField(model_attr='queue', faceted=True)
    queue = indexes.CharField(model_attr='queue', faceted=True, null=True)
    assigned_to = indexes.CharField(model_attr='assigned_to', faceted=True, null=True)
    #priority = indexes.IntegerField(model_attr='priority', faceted=True, null=True)
    tags = indexes.MultiValueField(faceted=True, null=True)

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    #def prepare_assigned_to(self, obj):
    #    if obj.assigned_to:
    #        return obj.assigned_to.username 

    def prepare_priority(self, obj):
        priorities = {1:'critical', 2:'high', 3:'normal', 4:'low', 5:'very low'}
        return priorities[obj.priority]

    #def prepare_queue(self, obj):
    #    return obj.queue.title.replace(' ', '') 

    def get_model(self):
        return Ticket

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
        return self.get_model().objects.all()
