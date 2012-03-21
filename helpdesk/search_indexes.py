from haystack import indexes
from helpdesk.models import Ticket


class TicketIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='description', null=True)
    followup_str = indexes.CharField(model_attr='followup_str')
    title = indexes.CharField(model_attr='title', faceted=True)
    assigned_to = indexes.CharField(model_attr='assigned_to', null=True, faceted=True)
    submitted_by = indexes.CharField(null=True, faceted=True)
    priority_str = indexes.CharField(model_attr='priority_str', faceted=True)
    status_str = indexes.CharField(model_attr='status_str', faceted=True)
    queue = indexes.CharField(model_attr='queue', faceted=True)
    tags = indexes.MultiValueField(faceted=True, null=True)

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_model(self):
        return Ticket

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
        return self.get_model().objects.all()
