from haystack import indexes
from helpdesk.models import Ticket


class TicketIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    assigned_to = indexes.CharField(model_attr='assigned_to', null=True)
    priority_str = indexes.CharField(model_attr='priority_str')
    queue = indexes.CharField(model_attr='queue')
    tags = indexes.MultiValueField(faceted=True, null=True)

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    #def prepare_assigned_to(self, obj):
    #    if obj.assigned_to:
    #        return obj.assigned_to.username 

    def get_model(self):
        return Ticket

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
        return self.get_model().objects.all()
