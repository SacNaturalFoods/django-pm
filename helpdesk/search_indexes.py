import datetime
from haystack import indexes
from helpdesk.models import Ticket


class TicketIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    queue = indexes.CharField(model_attr='queue', faceted=True)
    assigned_to = indexes.CharField(model_attr='assigned_to', faceted=True, null=True)
    priority = indexes.IntegerField(model_attr='priority', faceted=True, null=True)
    tags = indexes.MultiValueField()

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_model(self):
        return Ticket

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
        return self.get_model().objects.all()
